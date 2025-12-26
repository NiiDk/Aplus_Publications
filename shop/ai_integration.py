from .models import Textbook
from django.db.models import Q

class AcademicAIService:
    """
    Skeleton for AI-driven academic enhancements.
    Prepared for integration with LLMs (e.g., GPT-4) or Recommendation Engines.
    """

    @staticmethod
    def get_recommendations(user, textbook=None, limit=5):
        """
        Skeleton for Personalized Recommendations.
        Future Logic: Collaborative filtering or Content-based filtering 
        based on user's Academic Level and Subject interests.
        """
        # Placeholder: Return popular books in the same level for now
        if textbook:
            return Textbook.objects.filter(
                academic_level=textbook.academic_level,
                subject=textbook.subject
            ).exclude(id=textbook.id)[:limit]
        
        if user.is_authenticated:
            # Future: Query user's profile/history for interests
            return Textbook.objects.all()[:limit]
            
        return Textbook.objects.none()

    @staticmethod
    def smart_search_hook(query_text):
        """
        Hook for NLP-based Smart Search.
        Future Logic: Vector search (e.g., Pinecone/Weaviate) or Semantic search.
        """
        # For now, return a standard Q object
        return Q(title__icontains=query_text) | Q(description__icontains=query_text)

    @staticmethod
    def prepare_analytics_payload(user, action, target_object):
        """
        Structures data for AI training models.
        Captures: User Role, Subject context, and Action type.
        """
        payload = {
            "user_id": user.id if user.is_authenticated else None,
            "user_role": getattr(user, 'role', 'GUEST'),
            "action": action,
            "target_type": target_object.__class__.__name__,
            "target_id": getattr(target_object, 'id', None),
            "academic_context": {
                "level": getattr(target_object, 'academic_level_id', None),
                "subject": getattr(target_object, 'subject_id', None),
            }
        }
        return payload
