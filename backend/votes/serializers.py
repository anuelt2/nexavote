"""
votes/serializers.py
Serializers for the Vote and VoteAuditLog models.
"""
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Vote, VoteAuditLog
from elections.models import Candidate
from users.models import VoterProfile


class VoteCastSerializer(serializers.ModelSerializer):
    """
    Serializer for casting a vote.
    Only requires candidate_id, voter is automatically set from request.user.
    """
    candidate_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Vote
        fields = ['candidate_id']
    
    def validate_candidate_id(self, value):
        """
        Validate that the candidate exists and the election is open.
        """
        try:
            candidate = Candidate.objects.get(id=value)
        except Candidate.DoesNotExist:
            raise serializers.ValidationError("Invalid candidate ID.")
        
        if not candidate.election.is_open():
            raise serializers.ValidationError(
                "Cannot vote: Election is not currently open."
            )
        
        return value
    
    def validate(self, attrs):
        """
        Additional validation to check if user has already voted.
        """
        candidate_id = attrs['candidate_id']
        candidate = Candidate.objects.get(id=candidate_id)
        
        # Get voter from request context
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        
        try:
            voter = VoterProfile.objects.get(user=request.user)
        except VoterProfile.DoesNotExist:
            raise serializers.ValidationError("Voter profile not found.")
        
        # Check if user has already voted in this election
        if Vote.objects.filter(
            voter=voter,
            candidate__election=candidate.election.id
        ).exists():
            raise serializers.ValidationError(
                "You have already voted in this election."
            )
        
        attrs['voter'] = voter
        attrs['candidate'] = candidate
        return attrs
    
    def create(self, validated_data):
        """
        Create a new vote instance.
        """
        candidate_id = validated_data.pop('candidate_id')
        candidate = validated_data.pop('candidate')
        voter = validated_data.pop('voter')
        
        try:
            vote = Vote.objects.create(
                voter=voter,
                candidate=candidate,
                **validated_data
            )
            return vote
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))


class VoteDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying vote details.
    """
    voter_email = serializers.CharField(source='voter.user.email', read_only=True)
    candidate_name = serializers.SerializerMethodField()
    election_title = serializers.CharField(source='election.title', read_only=True)
    election_id = serializers.UUIDField(source='election.id', read_only=True)
    
    class Meta:
        model = Vote
        fields = [
            'id', 'voter_email', 'candidate_name', 'election_title', 
            'election_id', 'vote_hash', 'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'vote_hash', 'created_at']
    
    def get_candidate_name(self, obj):
        """
        Return full candidate name.
        """
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"


class VoteResultSerializer(serializers.Serializer):
    """
    Serializer for election results.
    """
    candidate_name = serializers.CharField()
    vote_count = serializers.IntegerField()


class ElectionResultsSerializer(serializers.Serializer):
    """
    Serializer for complete election results.
    """
    election_id = serializers.UUIDField()
    election_title = serializers.CharField()
    total_votes = serializers.IntegerField()
    results = VoteResultSerializer(many=True)


class VoterParticipationSerializer(serializers.Serializer):
    """
    Serializer for voter participation statistics.
    """
    total_invited_voters = serializers.IntegerField()
    unique_voters_participated = serializers.IntegerField()
    participation_rate = serializers.FloatField()
    votes_per_election = serializers.DictField()
    total_votes_cast = serializers.IntegerField()


class VoteAuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for vote audit logs.
    """
    performed_by_email = serializers.CharField(
        source='performed_by.email', 
        read_only=True
    )
    vote_details = serializers.SerializerMethodField()
    
    class Meta:
        model = VoteAuditLog
        fields = [
            'id', 'action', 'performed_by_email', 'details', 
            'ip_address', 'created_at', 'vote_details'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_vote_details(self, obj):
        """
        Return basic vote information.
        """
        return {
            'vote_id': str(obj.vote.id),
            'voter_email': obj.vote.voter.user.email,
            'candidate_name': f"{obj.vote.candidate.first_name} {obj.vote.candidate.last_name}",
            'election_title': obj.vote.election.title
        }


class VoteVerificationSerializer(serializers.Serializer):
    """
    Serializer for vote verification.
    """
    vote_hash = serializers.CharField(max_length=64)
    
    def validate_vote_hash(self, value):
        """
        Validate that the vote hash exists.
        """
        if not Vote.objects.filter(vote_hash=value).exists():
            raise serializers.ValidationError("Invalid vote hash.")
        return value