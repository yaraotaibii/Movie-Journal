from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from movies_database import Genres, Base, Movies, User

engine = create_engine('sqlite:///movieswithusers.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


genre1 = Genres(name = "Family")

session.add(genre1)
session.commit()

user1 = User(name = "Yara", email = "yara.alotaibi@gmail.com ", picture = "https://m.media-amazon.com/images/M/MV5BMjUwMjMxNTY0M15BMl5BanBnXkFtZTgwOTI0NjQzNDM@._V1_SY1000_CR0,0,643,1000_AL_.jpg")

session.add(user1)
session.commit()

movie1 = Movies(name = "Matilda", synopsis = "Story of a wonderful little girl, who happens to be a genius, and her wonderful teacher vs. the worst parents ever and the worst school principal imaginable.", release_date = "1996", poster = "https://i.pinimg.com/originals/0d/a9/39/0da93956f12d6a37a8172676401302dc.jpg", genre = genre1, user = user1)

session.add(movie1)
session.commit()

movie2 = Movies(name = "Home Alone", synopsis = "An eight-year-old troublemaker must protect his house from a pair of burglars when he is accidentally left home alone by his family during Christmas vacation.", release_date = "1990", poster = "http://www.barnsleyhouse.com/wp-content/uploads/2018/10/Home-Alone.jpg", genre = genre1, user = user1)

session.add(movie2)
session.commit()

##########################

genre2 = Genres(name = "Action")

session.add(genre2)
session.commit()

movie3 = Movies(name = "Mile 22", synopsis = "An elite American intelligence officer, aided by a top-secret tactical command unit, tries to smuggle a mysterious police officer with sensitive information out of Indonesia.", release_date = "2018", poster = "https://m.media-amazon.com/images/M/MV5BNzUyODk4OTkxNF5BMl5BanBnXkFtZTgwMzY0MDgzNTM@._V1_.jpg", genre = genre2, user = user1)

session.add(movie3)
session.commit()

movie4 = Movies(name = "John Wick", synopsis = "An ex-hit-man comes out of retirement to track down the gangsters that killed his dog and took everything from him.", release_date = "2014", poster = "https://i0.wp.com/www.pissedoffgeek.com/wordpress/wp-content/uploads/2015/01/John-Wick-One-Sheet.jpg?resize=689%2C1024", genre = genre2, user = user1)

session.add(movie4)
session.commit()

##########################

genre3 = Genres(name = "Comedy")

session.add(genre3)
session.commit()

movie5 = Movies(name = "Tag", synopsis = "A small group of former classmates organize an elaborate, annual game of tag that requires some to travel all over the country.", release_date = "2014", poster = "https://i.pinimg.com/originals/74/d5/d4/74d5d4e6f35f561a2d089da258bc3693.jpg", genre = genre3, user = user1)

session.add(movie5)
session.commit()

movie6 = Movies(name = "How to Steal a Million", synopsis = "Romantic comedy about a woman who must steal a statue from a Paris museum to help conceal her father's art forgeries, and the man who helps her.", release_date = "1966", poster = "https://images3.static-bluray.com/movies/uvcovers/3876_front.jpg?t=1390076980", genre = genre3, user = user1)

session.add(movie6)
session.commit()

movie23 = Movies(name = "Bride Wars", synopsis = "Two best friends become rivals when they schedule their respective weddings on the same day.", release_date = "2009", poster = "https://m.media-amazon.com/images/M/MV5BMTUyNTg2OTUwN15BMl5BanBnXkFtZTgwNzEzMzg5MTI@._V1_.jpg", genre = genre3, user = user1)

session.add(movie23)
session.commit()

##########################

genre4 = Genres(name = "Horror")

session.add(genre4)
session.commit()

movie7 = Movies(name = "The Strangers", synopsis = "A young couple staying in an isolated vacation home are terrorized by three unknown assailants.", release_date = "2008", poster = "https://i.pinimg.com/originals/92/d3/e7/92d3e7af1c966ac1a01c43ab4ed79cc4.jpg", genre = genre4, user = user1)

session.add(movie7)
session.commit()

movie8 = Movies(name = "It", synopsis = "In the summer of 1989, a group of bullied kids band together to destroy a shape-shifting monster, which disguises itself as a clown and preys on the children of Derry, their small Maine town.", release_date = "2017", poster = "https://i.pinimg.com/originals/b7/98/6f/b7986fd15b8305fee4ecacdd035eb972.jpg", genre = genre4, user = user1)

session.add(movie8)
session.commit()

##########################

genre5 = Genres(name = "Sci Fi")

session.add(genre5)
session.commit()

movie9 = Movies(name = "Doctor Strange", synopsis = "While on a journey of physical and spiritual healing, a brilliant neurosurgeon is drawn into the world of the mystic arts.", release_date = "2016", poster = "https://m.media-amazon.com/images/M/MV5BNjgwNzAzNjk1Nl5BMl5BanBnXkFtZTgwMzQ2NjI1OTE@._V1_.jpg", genre = genre5, user = user1)

session.add(movie9)
session.commit()

movie10 = Movies(name = "Avengers: Infinity War", synopsis = "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe.", release_date = "2018", poster = "https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_.jpg", genre = genre5, user = user1)

session.add(movie10)
session.commit()

##########################

genre6 = Genres(name = "Fantasy")

session.add(genre6)
session.commit()

movie11 = Movies(name = "Harry Potter and the Sorcerer's Stone", synopsis = "An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.", release_date = "2001", poster = "https://vignette.wikia.nocookie.net/transcripts/images/5/5c/Harry_Potter_and_the_Philosopher%27s_Stone_-_Theatrical_Poster.jpg/revision/latest?cb=20170130065413", genre = genre6, user = user1)

session.add(movie11)
session.commit()

movie12 = Movies(name = "Mary Poppins", synopsis = "In turn of the century London, a magical nanny employs music and adventure to help two neglected children become closer to their father.", release_date = "1964", poster = "https://vignette.wikia.nocookie.net/goldenthroats/images/7/78/Marypoppins.jpg/revision/latest?cb=20150922213822", genre = genre6, user = user1)

session.add(movie12)
session.commit()

##########################

genre7 = Genres(name = "Mystery")

session.add(genre7)
session.commit()

movie13 = Movies(name = "Zodiac", synopsis = "In the late 1960s/early 1970s, a San Francisco cartoonist becomes an amateur detective obsessed with tracking down the Zodiac Killer, an unidentified individual who terrorizes Northern California with a killing spree.", release_date = "2007", poster = "https://i.pinimg.com/originals/2c/14/10/2c141086f6539245de15152f48db5959.jpg", genre = genre7, user = user1)

session.add(movie13)
session.commit()

movie14 = Movies(name = "Rear Window", synopsis = "A wheelchair-bound photographer spies on his neighbors from his apartment window and becomes convinced one of them has committed murder.", release_date = "1954", poster = "https://i.pinimg.com/originals/e4/b9/dd/e4b9dd0cdcf6e13e8babe558da48464f.jpg", genre = genre7, user = user1)

session.add(movie14)
session.commit()

##########################

genre8 = Genres(name = "Adventure")

session.add(genre8)
session.commit()

movie15 = Movies(name = "The Revenant", synopsis = "A frontiersman on a fur trading expedition in the 1820s fights for survival after being mauled by a bear and left for dead by members of his own hunting team.", release_date = "2015", poster = "https://images-na.ssl-images-amazon.com/images/I/A1BjliXNDPL._SL1500_.jpg", genre = genre8, user = user1)

session.add(movie15)
session.commit()

movie16 = Movies(name = "127 Hours", synopsis = "An adventurous mountain climber becomes trapped under a boulder while canyoneering alone near Moab, Utah and resorts to desperate measures in order to survive.", release_date = "2010", poster = "https://m.media-amazon.com/images/M/MV5BMTc2NjMzOTE3Ml5BMl5BanBnXkFtZTcwMDE0OTc5Mw@@._V1_.jpg", genre = genre8, user = user1)

session.add(movie16)
session.commit()

movie21 = Movies(name = "Pirates of the Caribbean: The Curse of the Black Pearl", synopsis = "Blacksmith Will Turner teams up with eccentric pirate \"Captain\" Jack Sparrow to save his love, the governor's daughter, from Jack's former pirate allies, who are now undead.", release_date = "2003", poster = "https://www.dvdsreleasedates.com/posters/800/P/Pirates-of-the-Caribbean-The-Curse-of-the-Black-Pearl-movie-poster.jpg", genre = genre8, user = user1)

session.add(movie21)
session.commit()

##########################

genre9 = Genres(name = "Drama")

session.add(genre9)
session.commit()

movie17 = Movies(name = "Gone with the Wind", synopsis = "A manipulative woman and a roguish man conduct a turbulent romance during the American Civil War and Reconstruction periods.", release_date = "1939", poster = "https://i.pinimg.com/originals/ce/ce/b7/ceceb7c9d235eb3808a2c7d0460af9eb.jpg", genre = genre9, user = user1)

session.add(movie17)
session.commit()

movie18 = Movies(name = "The Help", synopsis = "An aspiring author during the civil rights movement of the 1960s decides to write a book detailing the African American maids' point of view on the white families for which they work, and the hardships they go through on a daily basis.", release_date = "2011", poster = "https://m.media-amazon.com/images/M/MV5BMTM5OTMyMjIxOV5BMl5BanBnXkFtZTcwNzU4MjIwNQ@@._V1_.jpg", genre = genre9, user = user1)

session.add(movie18)
session.commit()

##########################

genre10 = Genres(name = "Thriller")

session.add(genre10)
session.commit()

movie19 = Movies(name = "Dial M for Murder", synopsis = "A tennis player frames his unfaithful wife for first-degree murder after she inadvertently hinders his plan to kill her.", release_date = "1954", poster = "https://cdn.shopify.com/s/files/1/0747/3829/products/HP2914_ee56f2ab-dcae-4eb8-91a6-dd992f25711c_1024x1024.jpg?v=1515504536", genre = genre10, user = user1)

session.add(movie19)
session.commit()

movie20 = Movies(name = "The Silence of the Lambs", synopsis = "A young FBI cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.", release_date = "1991", poster = "https://m.media-amazon.com/images/M/MV5BNjNhZTk0ZmEtNjJhMi00YzFlLWE1MmEtYzM1M2ZmMGMwMTU4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg", genre = genre10, user = user1)

session.add(movie20)
session.commit()

movie22 = Movies(name = "Secret Window", synopsis = "A successful writer in the midst of a painful divorce is stalked at his remote lake house by a would-be scribe who accuses him of plagiarism.", release_date = "2004", poster = "http://static.tvgcdn.net/feed/1/320/118278320.jpg", genre = genre10, user = user1)

session.add(movie22)
session.commit()

##########################

print "Added movies!!"
