"""
Results models for tracking test performance and analytics.
"""
import uuid
from django.db import models
from django.conf import settings


class Result(models.Model):
    """
    Detailed result model for test sessions.
    This provides a denormalized view for easier analytics.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results'
    )
    test = models.ForeignKey(
        'tests.Test',
        on_delete=models.CASCADE,
        related_name='results'
    )
    test_session = models.OneToOneField(
        'tests.TestSession',
        on_delete=models.CASCADE,
        related_name='result'
    )
    
    # Scores
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    unanswered = models.IntegerField(default=0)
    
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField()
    
    # Timing
    time_limit_seconds = models.IntegerField()
    time_taken_seconds = models.IntegerField()
    
    # Rankings and percentiles (calculated periodically)
    rank = models.IntegerField(null=True, blank=True, help_text="Rank among all test takers")
    percentile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Percentile ranking"
    )
    accuracy = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Accuracy percentage (Correct / Answered)"
    )
    
    # Virtual Set Tracking
    set_number = models.IntegerField(default=1, help_text="The partition number of the bank")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'results'
        db_table = 'results'
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['test', '-score_percentage']),
            models.Index(fields=['-score_percentage']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name} - {self.score_percentage}%"
    
    @classmethod
    def create_from_session(cls, session):
        """Create a result from a completed test session."""
        total_questions = session.test.total_questions
        correct_answers = session.score or 0
        wrong_answers = len(session.answers) - correct_answers
        unanswered = total_questions - len(session.answers)
        
        # Calculate Accuracy: Correct / (Correct + Wrong) * 100
        answered_count = len(session.answers)
        if answered_count > 0:
            accuracy = (correct_answers / answered_count) * 100
        else:
            accuracy = 0.00
            
        result = cls.objects.create(
            user=session.user,
            test=session.test,
            test_session=session,
            total_questions=total_questions,
            correct_answers=correct_answers,
            wrong_answers=wrong_answers,
            unanswered=unanswered,
            score_percentage=session.percentage or 0,
            passed=session.passed or False,
            time_limit_seconds=session.time_limit_seconds,
            time_taken_seconds=session.time_spent_seconds,
            accuracy=accuracy,
            set_number=session.set_number
        )
        
        return result


class PerformanceAnalytics(models.Model):
    """
    Aggregated analytics for user performance.
    Updated periodically or after each test.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Overall statistics
    total_tests_taken = models.IntegerField(default=0)
    total_tests_passed = models.IntegerField(default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    highest_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lowest_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Time statistics
    average_time_taken = models.IntegerField(default=0, help_text="Average time in seconds")
    total_time_spent = models.IntegerField(default=0, help_text="Total time in seconds")
    
    # Answer statistics
    average_questions_answered = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        help_text="Average number of questions answered per test"
    )
    
    # Difficulty breakdown
    easy_correct = models.IntegerField(default=0)
    easy_total = models.IntegerField(default=0)
    medium_correct = models.IntegerField(default=0)
    medium_total = models.IntegerField(default=0)
    hard_correct = models.IntegerField(default=0)
    hard_total = models.IntegerField(default=0)
    
    # Last updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'results'
        db_table = 'performance_analytics'
        verbose_name = 'Performance Analytics'
        verbose_name_plural = 'Performance Analytics'
    
    def __str__(self):
        return f"Analytics for {self.user.username}"
    
    def update_from_result(self, result):
        """Update analytics based on a new result."""
        from decimal import Decimal
        
        self.total_tests_taken += 1
        if result.passed:
            self.total_tests_passed += 1
        
        # Update average score - convert to Decimal for consistent math
        if self.total_tests_taken == 1:
            self.average_score = result.score_percentage
            self.average_accuracy = result.accuracy
        else:
            # Weighted average calculation with Decimal type
            total_score = (Decimal(str(self.average_score)) * (self.total_tests_taken - 1)) + Decimal(str(result.score_percentage))
            self.average_score = total_score / self.total_tests_taken
            
            total_accuracy = (Decimal(str(self.average_accuracy)) * (self.total_tests_taken - 1)) + Decimal(str(result.accuracy))
            self.average_accuracy = total_accuracy / self.total_tests_taken
        
        # Update highest/lowest scores
        if result.score_percentage > self.highest_score:
            self.highest_score = result.score_percentage
        
        if self.lowest_score is None or result.score_percentage < self.lowest_score:
            self.lowest_score = result.score_percentage
        
        # Update time statistics
        self.total_time_spent += result.time_taken_seconds
        self.average_time_taken = self.total_time_spent // self.total_tests_taken
        
        # Update questions answered statistics
        from decimal import Decimal
        questions_answered = result.correct_answers + result.wrong_answers
        if self.total_tests_taken == 1:
            self.average_questions_answered = Decimal(str(questions_answered))
        else:
            total_answered = (Decimal(str(self.average_questions_answered)) * (self.total_tests_taken - 1)) + Decimal(str(questions_answered))
            self.average_questions_answered = total_answered / self.total_tests_taken
        
        self.save()
    
    def recalculate_from_results(self):
        """Recalculate all analytics from existing results."""
        results = Result.objects.filter(user=self.user).order_by('created_at')
        
        if not results.exists():
            # Reset to defaults if no results
            self.total_tests_taken = 0
            self.total_tests_passed = 0
            self.average_score = 0
            self.average_accuracy = 0
            self.highest_score = 0
            self.lowest_score = None
            self.average_time_taken = 0
            self.total_time_spent = 0
            self.average_questions_answered = 0
            self.save()
            return
        
        # Reset counters
        self.total_tests_taken = 0
        self.total_tests_passed = 0
        total_score = 0
        total_accuracy = 0
        self.highest_score = 0
        self.lowest_score = None
        self.total_time_spent = 0
        total_questions_answered = 0
        
        # Iterate through all results
        for result in results:
            self.total_tests_taken += 1
            if result.passed:
                self.total_tests_passed += 1
            
            total_score += float(result.score_percentage)
            total_accuracy += float(result.accuracy)
            
            if result.score_percentage > self.highest_score:
                self.highest_score = result.score_percentage
            
            if self.lowest_score is None or result.score_percentage < self.lowest_score:
                self.lowest_score = result.score_percentage
            
            self.total_time_spent += result.time_taken_seconds
            total_questions_answered += (result.correct_answers + result.wrong_answers)
        
        # Calculate averages
        if self.total_tests_taken > 0:
            self.average_score = total_score / self.total_tests_taken
            self.average_accuracy = total_accuracy / self.total_tests_taken
            self.average_time_taken = self.total_time_spent // self.total_tests_taken
            self.average_questions_answered = total_questions_answered / self.total_tests_taken
        
        self.save()
