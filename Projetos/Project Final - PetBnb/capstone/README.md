# PetBnb
>*This project was developed for the CS50W course at Harvard*

## Distinctiveness and Complexity
I spent a lot of time thinking up an idea for the final project that would meet the *Distinctiveness and Complexity* requirements. Looking at the work done by other CS50 students, I realized that I would have to surpass myself because all the projects I saw are very good. So I started thinking about producing something that could be considered "almost" a commercial product, something that would really help to solve a real problem. That's when I needed to travel and I started looking for hotels for dogs here in my city to host my dog and I realized that it was very difficult to find one with enough information and good references, so I decided to program the PetBnb.
Regarding complexity, I tried to expand the knowledge transmitted in the classes and also to seek to learn concepts, tools, techniques and frameworks that were not presented in the classes. That's why I decided to invest time and effort in developing a responsive design, applying javascript plugins and using Django's *Class Based Views* in order to raise the bar on the knowledge I gained in class.
This increased the scope, complexity and time I invested to finish the project but I think this effort was worth it because, starting from *ZERO* knowledge in Python/Django and observing what I produced during the course, I feel confident to work on any project from software that uses these technologies.

## What’s contained in each file I created.
There are many files that it is impossible to describe them all here, but I can mention some more important ones:
- I divided the project into several Apps because I realized that this is an industry standard and it provides organization and facilitates the understanding of the project.
- Likewise, I centralized the images in the "media" folder and static files (css, js, etc) in the "staticfiles" folder, thus creating a central point of access to this information.
- In some cases, instead of returning the complete Model to the View, I chose to create classes that represent this return. Examples are the classes: booking/models/ReviewResult.py which represents a review and the list of replies for this review.
- Created the user/utils/token_generator.py class to generate activation tokens and password resets for users, thus ensuring more security.
- In user/templatetags/petbnb_extras.py I created the [inclusion tags](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#inclusion-tags) which are a kind of "back-end" for the templatetags. Thus, templatetags work as a kind of reusable component. This streamlines the development process and avoids code duplication.
  - A problem I found using templatetags was that when a templatetag is used inside another templatetag the *request* object can be found in *context.request* instead of *context['request']*. This is a behavior that I found strange and it took me a long time to figure out the problem, so I think it's important to show the code here. I managed to solve it by creating the following function:
  
    ```python
     # When a template is inside another template, the request can be found at context.request intead of context['request']. So I try to get the request from the context and if it fails, I get the request from the request parameter
    def get_request_from_context(context):    
        request = None
        if hasattr(context, 'request'):
           request = context.request
        else:
            request = context['request']
        return request
    ``` 
    This way this code works for both cases, when the templatetag is used directly inside the page or when it is used inside another templatetag.

## How to run your application
To facilitate the test I'm providing the application with some records previously created in the database. So to run the application you must:
- Clone it from [github](https://link)
- Go to applications folder `cd "TheFolder\WhereYouClonedIt"`
- Run It `py.exe manage.py runserver`
  - Users already created
    - User1 - Password: 1234
 
If you want to register a new user, note that, right after saving the registration, the URL to activate the registration will be made available in the console, typically this URL would be sent by email to the user. In order to access the system with the registered user, you must access this URL at least once.

## Additional information to the CS50W staff.

----------


## PetBnb é como um AirBnb, só que para pets.
Pet owners often need to host their pets in pet-shops when they need to work, travel or just for pets to play and interact with other animals. The PetBnB system offers features very similar to those offered by AirBnb.

## Overview de Funcionalidades 
On PetBnb, users who need accommodation for their pets can search for hosting locations by filtering by date and type of pet (dog, cat, bird, etc). These users can also visit a page containing all the information about the hosting place and the place owner. This page displays descriptions of the service offered, a location map, photos of the location, dates available for accommodation and reviews from other users. This way, the person who is looking for accommodation for their pet can choose the best place and host.

Likewise, people who want to become hosts and host other people's pets can register and include their personal information and location information such as photos, and available dates. When a pet owner requests accommodation, the host has the option of accepting or rejecting the accommodation as well as providing a justification in case they reject it.

After the end of the accommodation, the pet owner can visit the host's page and leave an evaluation of the services.

## Technical details

In this project I had the opportunity to exercise areas of knowledge that I still had little knowledge of and to explore ideas and concepts that I had not used before but was curious to learn. 

### Project structure (apps)
I chose to separate the system concepts into different apps. I realized that this is a common practice in large projects and that it facilitates the organization and understanding of the project. I had some problems getting the projects to reference each other avoiding circular references but the challenge was important for me to learn about it.
### Frontend
I invested a lot of time and effort to make the system completely responsive, beatiful and minimalist. I used jQuery and javascript plugins to improve the user experience in some cases. Of the plugins and frameworks I used, I can cite some here that were very useful:
- Bootstrap: Used to make the layout responsive using the concept of rows and cols.
- DataTables: Used to show data in tables and make tables responsive.
- Date Range Picker: Used to improve user experience when selecting dates to search for accommodation.
- Owl Carousel: Used to provide an image carousel on the host's profile page.
- Fancybox: Used to improve the user experience when viewing photos on the website
- Lazyest Load: Used to load the website images on demand.
- Font-Awesome: Used for icons.
- RateYo: Used to improve the experience when the user is going to rate the host with 1 or 5 stars.
- Google Maps Api: Used to display a map, coordinates and routes to the Host address.
- and others...


### Users Profiles
There are two profiles in the system:
- Client: It is the user who owns a pet and is looking for accommodation.
- Server: It is the user who is the host and will host the pets at your location.

When a user registers in the system, a record is automatically created in the `user_user` table (which represents the user itself) and also a record in the `user_profileclient` table (which represents the profile of this user as client). The creation of a record for the Server Profile (`user_profileserver` table) is optional, that is, a ServerProfile will only be created if the user wants to offer its hosting location.

To automate this process that creates a ProfileClient whenever a User is created, I used the [Django signals](https://docs.djangoproject.com/en/3.2/topics/signals/) feature. This way, I guarantee that these two objects will always be created and associated with each other.


### Django Custom Tags
Another feature of Django that I learned and helped me a lot was the use of [Custom Tags](https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/). Custom Tags make development much easier because they allow you to develop isolated blocks (templates) and reuse them whenever I need, in this way, I develop the template only once and avoid unnecessary code duplication.
I created custom tags for the footer, main navigation bar, secondary navigation bar, rating listing and for the form which create a new rating. I had some challenges in using Custom Tags that need to manipulate the DOM via javascript because, whenever a custom tag is requested via AJAX, it is necessary to "rebind" the javascript events used by the Custom Tag. Winning this challenge was important for me to better understand how the javascript chain of events occurs during the lifecycle of a request.

### Class Based Views
Unlike other projects developed for the CS50W 2021, I chose to use [Django's Class Based Views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/). I made this choice after reading some tutorials and reviewing the code for Python/Django projects on github, I realized that the vast majority use *Class Based Views* and I figured this was a "pattern" used by Python/Django developers. Using this feature was interesting because it increased my knowledge of Django, however, this feature didn't please me. I found that it creates a very high abstraction and distances the developer from the fundamental concept of web development which is the request/response pattern. I also found that *Class Based Views* make it difficult to understand the flow of a request and make the View code harder to read. This perception of mine will probably be mitigated as I further deepen my knowledge of Django and *Class Based Views*, however, with this first experience I had, it seems to me that the *Class Based Views* feature brings more benefits to projects that do intensive use of inheritance and mixins, which wasn't my case.

## Conclusions
I'm very happy that starting from scratch in Python and Django related knowledge I was able to quickly produce a system that, with a few tweaks, could potentially be used in production in a real commercial application. Therefore, I believe that all the effort put into these projects was very worthwhile as I finish the course with much more knowledge than when I started and with a strong desire to learn more about Python.
