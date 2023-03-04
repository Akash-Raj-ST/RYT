<h1 align="center"><b>R Y T</b></h1>
<h2 align="center"><b>Review Your Tour</b></h2>

Using this you can share your personal reviews about a place(Images,Text,Tags) under that specific place.<br>
It has a huge data collection of different places with their info and the places inside of it is mapped in it.<br>
It can also be used to learn about a place and see other peoples review about it.<br>
It has a profile section so that you can see whether other people have been, all their reviews and the review that they have liked<br>
Easy filtering options to filter places<br>
Search option is available to search a particular places or people.<br>
<br><br>


<h1>How to Use:</h1>

<h3>Prerequisites:</h3>
    <ol>
        <li>Django</li>
        <li>Postgresql</li>
    </ol>

<h4>Step 1: Clone the repo</h4>

<h4>Step 2: Setup the postgresql DB</h4>

[How to setup postgresql in windows](https://www.youtube.com/watch?v=RAFZleZYxsc)

<li>goto RYT/ RYT/ setting.py and replace DB_PASSWORD,DB_USER_NAME,DJANGO_SECRET_KEY with your own.</li>
<li>goto RYT directory and run the following commands:</li>

`python manage.py makemigrations`<br>
`python manage.py migrate`<br>
This will update the tables from api/models.py to DB.


<h4>step 3: Add the place data to DB.</h4>
<li>The following steps is to add the collections of place data to DB.</li>
<li>goto RYT/ admin.py and run the python script.</li>
<li>Follow the instructions its pretty easy from that.</li>

<h4>step 4: Start the server</h4>

`python manage.py runserver`<br>
This will start the development server in localhost.

<h4>step 5: Enjoy the site.</h4>

Open localhost in your broswer(chrome recommended) and <b>have fun.</b>

<br>
<b>You have come so far. If you like this make sure to leave a STAR :)</b>
