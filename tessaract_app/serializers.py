from django.db import models
from django.db.models.fields import Field
from rest_framework import serializers
from rest_framework.utils import field_mapping

from . models import *

class userserilizer(serializers.ModelSerializer):
    class Meta:
        model = Users  # specify the model
        fields = '__all__'

class projectserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblProjects  # specify the model
        fields = '__all__'


class Drawingserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblDrawings  # specify the model
        fields = '__all__'

class Specificationserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblSpecifications  # specify the model
        fields = ('id','current_revision_id')

class Spec_urlserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblSpecSections  # specify the model
        fields = ('id','attachment')

class RFIserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblRfis  # specify the model
        fields = '__all__'

class RFIAnsserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblRfiAnswers  # specify the model
        fields = '__all__'

class RFIAttachserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblRfiAttachments  # specify the model
        fields = ('id','closeout_attachment_url')

class RFIQuesAttachserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblRfiQuestions  # specify the model
        fields = '__all__'

class RFIQuesPathserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblRfiQuestionsAttachments  # specify the model
        fields = ('id','closeout_attachment_url')

class Indexerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblProjectIndex  # specify the model
        fields = ('id','title')

class ApprovedSubmittalserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblApproveSubmittals  # specify the model
        fields = '__all__'

class workflowSubmittalserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblSubmittalWorkflow  # specify the model
        fields = '__all__'
class workflowSubmittalserilizers(serializers.ModelSerializer):
    class Meta:
        model = TblSubmittalWorkflow  # specify the model
        fields = '__all__'

class submittalsAttachmentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblSubmittalAttachments  # specify the model
        fields = '__all__'

class CloseoutItemsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblCloseoutItems  # specify the model
        fields = '__all__'

class CloseoutAttachmentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblCloseoutItemUploads  # specify the model
        fields = '__all__'
class TblindexSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblProjectIndex  # specify the model
        fields = '__all__'

class CoverPageSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblCoverPages  # specify the model
        fields = '__all__'
class TableContetserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblIndexPages  # specify the model
        fields = '__all__'

class TblManualSerilizer(serializers.ModelSerializer):
    class Meta:
        model = TblCloseoutManual  # specify the model
        fields = '__all__'

class specDivision(serializers.ModelSerializer):
    class Meta:
        model = TblSpecSectionDivisions  # specify the model
        fields = '__all__'


class tradeserilizer(serializers.ModelSerializer):
    class Meta:
        model = TblTrades  # specify the model
        fields = '__all__'