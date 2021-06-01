from django.forms import ModelForm
from django import forms

from .models import Listing, Bid, Comment, Category

class NewListingForm(forms.Form):

    # <input name="title" type="text" class="form-control" id="title" aria-describedby="titleHelp" /> 
    title = forms.CharField(label='title', required=True, 
            widget=forms.TextInput(attrs={'id': 'title',
                                            'class': 'form-control', 
                                            'aria-describedby': 'titleHelp'}))

    #<textarea name="description" type="text"  class="form-control" id="description" aria-describedby="descriptionHelp" rows="8"></textarea>
    description = forms.CharField(label='description', required=True, min_length=10, 
                  widget=forms.Textarea(attrs={'id':'description',
                                                'class': 'form-control', 
                                                'rows':'8',
                                                'aria-describedby': 'descriptionHelp'}))
    
    #<input name="start_bid" type="number" min="0" step="0.01" class="form-control" id="startBid" aria-describedby="startBidHelp" />
    start_bid = forms.CharField(label="start_bid",
                widget=forms.NumberInput(attrs={'id':'start_bid',
                                                'class': 'form-control',
                                                'aria-describedby': 'startBidHelp',
                                                'step':'0.01', 'min':'0'}))
    
    #<input name="image_url" type="text" class="form-control" id="imageURL" aria-describedby="imageURLHelp" />
    image_url = forms.CharField(label="image_url", 
                widget=forms.URLInput(attrs={'id':'imageURL',
                                             'class': 'form-control',
                                             'aria-describedby': 'imageURLHelp'}))
    
    
    options = Category.objects.values_list('id', 'category')
    category = forms.ChoiceField(choices=options,
                        widget=forms.Select( attrs={'id':'imageURL',
                                                            'class': 'form-control',
                                                            'aria-describedby': 'imageURLHelp'}))