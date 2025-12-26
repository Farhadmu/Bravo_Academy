"""
Question models for IQ tests.
"""
import uuid
from django.db import models
from apps.tests.models import Test


class Question(models.Model):
    """
    Question model for IQ tests.
    Supports multiple choice questions.
    """
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    
    # Question content
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='mcq'
    )
    
    # Options stored as JSON
    # Format: [{"id": "a", "text": "Option A"}, {"id": "b", "text": "Option B"}, ...]
    options = models.JSONField(default=list, help_text="Answer options as JSON array")
    
    # Correct answer (stores the option ID, e.g., "a", "b", etc.)
    correct_answer = models.CharField(max_length=10)
    
    # Additional metadata
    difficulty_level = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    order = models.IntegerField(default=0, help_text="Display order within a test if not in a bank")
    bank_order = models.IntegerField(default=0, help_text="Global index in the unified question bank")
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'questions'
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['bank_order', 'order', 'created_at']
        indexes = [
            models.Index(fields=['test', 'order']),
            models.Index(fields=['bank_order']),
            models.Index(fields=['difficulty_level']),
        ]
    
    def __str__(self):
        return f"Question for {self.test.name} - {self.question_text[:50]}..."
    
    def get_correct_option_text(self):
        """Get the text of the correct answer option."""
        for option in self.options:
            if str(option.get('id')) == str(self.correct_answer):
                return option.get('text', '')
        return ''
    
    def validate_answer(self, answer_id):
        """Check if the provided answer is correct."""
        return str(answer_id) == str(self.correct_answer)


class QuestionImage(models.Model):
    """
    Optional images for questions.
    Some IQ test questions may include diagrams or images.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='questions/images/')
    caption = models.CharField(max_length=255, blank=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'questions'
        db_table = 'question_images'
        verbose_name = 'Question Image'
        verbose_name_plural = 'Question Images'
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"Image for {self.question}"


# Signals to keep test total_questions in sync
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Question)
def update_test_question_count_on_save(sender, instance, **kwargs):
    """Update the total_questions count on the parent Test (skip for banks)."""
    test = instance.test
    if test.is_bank:
        return
    actual_count = Question.objects.filter(test=test).count()
    if test.total_questions != actual_count:
        test.total_questions = actual_count
        test.save(update_fields=['total_questions'])

@receiver(post_delete, sender=Question)
def update_test_question_count_on_delete(sender, instance, **kwargs):
    """Update the total_questions count on the parent Test (skip for banks)."""
    test = instance.test
    if test.is_bank:
        return
    actual_count = Question.objects.filter(test=test).count()
    if test.total_questions != actual_count:
        test.total_questions = actual_count
        test.save(update_fields=['total_questions'])
