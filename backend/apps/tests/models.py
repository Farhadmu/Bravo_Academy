"""
Test models for managing IQ tests.
"""
import uuid
from django.db import models
from django.conf import settings


class Test(models.Model):
    """
    IQ Test model.
    Represents a test that users can take.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Test configuration
    duration_minutes = models.IntegerField(default=30, help_text="Duration in minutes")
    total_questions = models.IntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    passing_score = models.IntegerField(default=50, help_text="Passing score percentage")
    
    # Test type
    is_free_sample = models.BooleanField(default=False, help_text="Is this a free sample test?")
    is_bank = models.BooleanField(default=False, help_text="Is this a unified question bank?")
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tests'
    )
    
    class Meta:
        app_label = 'tests'
        db_table = 'tests'
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_free(self):
        """Check if test is free."""
        return self.is_free_sample or self.price == 0
    
    def get_question_count(self):
        """Get actual number of questions in this test."""
        return self.questions.count()


class TestSession(models.Model):
    """
    User's test session.
    Tracks when a user takes a test.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_sessions'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    # Session timing
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_limit_seconds = models.IntegerField(help_text="Time limit in seconds")
    time_spent_seconds = models.IntegerField(default=0, help_text="Actual time spent")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Answers stored as JSON
    # Format: {"question_id": "answer_option_id", ...}
    answers = models.JSONField(default=dict, blank=True)
    
    # Results
    score = models.IntegerField(null=True, blank=True, help_text="Number of correct answers")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    passed = models.BooleanField(null=True, blank=True)
    
    # Virtual Set Tracking
    set_number = models.IntegerField(default=1, help_text="The partition number of the bank")
    
    # Device tracking
    device_fingerprint = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        app_label = 'tests'
        db_table = 'test_sessions'
        verbose_name = 'Test Session'
        verbose_name_plural = 'Test Sessions'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-started_at']),
            models.Index(fields=['test', '-started_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name} - {self.started_at}"
    
    @property
    def is_completed(self):
        """Check if session is completed."""
        return self.status == 'completed'
    
    @property
    def is_in_progress(self):
        """Check if session is in progress."""
        return self.status == 'in_progress'
    
    def calculate_score(self):
        """
        Calculate score based on answers.
        Returns (score, percentage, passed).
        """
        from apps.questions.models import Question
        
        if not self.answers:
            return 0, 0.0, False
        
        # Optimize: Fetch all relevant questions in one query
        question_ids = self.answers.keys()
        
        if self.test.is_bank:
            start_range = (self.set_number - 1) * 100 + 1
            end_range = self.set_number * 100
            queryset = Question.objects.filter(
                id__in=question_ids, 
                test=self.test,
                bank_order__gte=start_range,
                bank_order__lte=end_range
            )
        else:
            queryset = Question.objects.filter(id__in=question_ids, test=self.test)
            
        questions_map = {str(q.id): q for q in queryset}
        
        correct_count = 0
        total_questions = 100 if self.test.is_bank else self.test.total_questions
        
        for question_id, answer_id in self.answers.items():
            question = questions_map.get(str(question_id))
            if question and str(question.correct_answer) == str(answer_id):
                correct_count += 1
        
        if total_questions == 0:
            return 0, 0.0, False
        
        percentage = (correct_count / total_questions) * 100
        passed = percentage >= self.test.passing_score
        
        return correct_count, round(percentage, 2), passed
    
    def submit_test(self):
        """Mark test as completed and calculate score."""
        from django.utils import timezone
        from apps.results.models import Result, PerformanceAnalytics
        
        self.status = 'completed'
        self.submitted_at = timezone.now()
        
        # Calculate time spent
        if self.started_at:
            time_diff = self.submitted_at - self.started_at
            self.time_spent_seconds = int(time_diff.total_seconds())
        
        # Calculate score
        score, percentage, passed = self.calculate_score()
        self.score = score
        self.percentage = percentage
        self.passed = passed
        
        self.save()

        # Create Result and update Analytics
        try:
            result = Result.create_from_session(self)
            analytics, _ = PerformanceAnalytics.objects.get_or_create(user=self.user)
            analytics.update_from_result(result)
        except Exception as e:
            # Log error but don't fail the submission
            print(f"Error creating result or updating analytics: {e}")
