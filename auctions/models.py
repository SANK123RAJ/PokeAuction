from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class category(models.Model):
    categoryname = models.CharField(max_length=64)  
    def __str__(self):
        return f"{self.categoryname}"

   


class Listings(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    time = models.DateTimeField()
    url = models.CharField(max_length=1000,blank= True)
    category = models.ForeignKey(category,on_delete=models.CASCADE,related_name="category")
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="owner")
    watchlist = models.ManyToManyField(User, blank=True, related_name="user",null=True)
    isactive = models.BooleanField(blank=True,null=True)
    def __str__(self):
        return f"{self.name}"
    

class Bids(models.Model):
    amount = models.IntegerField() 
    biddedlist = models.ForeignKey(Listings,on_delete=models.CASCADE,blank=True,related_name="bid") 
    bid_by = models.ForeignKey(User,blank=True,on_delete=models.CASCADE,related_name="placedbid")
    def __str__(self):
        return f"{self.amount} by {self.bid_by}"    


class Comment(models.Model):
    
    commenton = models.ForeignKey(Listings,on_delete=models.CASCADE,blank=True,related_name="allcomment") 
    commentby = models.ForeignKey(User,blank=True,on_delete=models.CASCADE,related_name="commented")
    commentmade = models.CharField(max_length=1000, blank=True, null=True)
    def __str__(self):
        return f"{self.commenton} by {self.commentby}"



'''


    def __str__(self):
        return f"by {self.comment_by} on {self.comment_on}"
    

class watchlist(models.Model):
    liste =  models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="watchlistedon")  
    watchlistedby = models.ForeignKey(User,on_delete=models.CASCADE,related_name="watchlistedby") 
    def __str__(self):
        return f"by {self.watchlistedby} did {self.liste}"    
    '''