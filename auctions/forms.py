from django import forms

from .models import Listing, Bid, Comment


class ListingForm(forms.ModelForm):
    class Meta: 
        model = Listing 
        fields = ["title", "description", "image_url", "category", "minimum_bid_amount",]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'image_url': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'minimum_bid_amount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),   
        }
        
class BidForm(forms.ModelForm):
    class Meta: 
        model = Bid
        fields = ["amount"]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control mb-3', "rows": 3}),
        }
        