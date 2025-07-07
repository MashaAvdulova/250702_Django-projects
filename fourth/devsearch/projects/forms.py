from django.forms import ModelForm
from .models import Projects

class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fiels = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']