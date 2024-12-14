from django.db import models
import pickle
# Create your models here.
class Applicant(models.Model):
    username = models.CharField(max_length=150,unique = True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 15)
    password = models.CharField(max_length= 200)
    resume = models.OneToOneField('Resume',on_delete = models.SET_NULL,null=False, blank= False)
    def __str__(self):
        return self.username

class Resume(models.Model):
    uploaded_by = models.ForeignKey(Applicant, on_delete=models.CASCADE,null=True,blank = True)
    is_batch_uplaod = models.BooleanField(default=False)
    resume_file = models.FileField(upload_to ='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add = True)
    resume_vector = models.BinaryField(null = True, blank = True)
    
    def save_vector(self,vector):
        self.resume_vector = pickle.dumps(vector)
        self.save()
    def get_vector(self):
        return pickle.loads(self.resume_vector) if self.resume_vector else None
    def __str__(self):
        return self.uploaded_by

