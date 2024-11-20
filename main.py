from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("__name__")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:password@localhost:3336/SHL"
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    namn = db.Column(db.String(50), unique = False, nullable = False)
    city = db.Column(db.String(50), unique = False, nullable = False)
    players = db.relationship("Player", backref = "team", lazy=True)

    def __str__(self):
        return f"Namn: {self.namn}, Stad: {self.city} "

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    namn = db.Column(db.String(50), unique = False, nullable = False)
    jersey = db.Column(db.Integer, unique = False, nullable = False)
    year = db.Column(db.Integer, unique = False, nullable = False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable = True)
    
    def __str__(self):
        return f"Namn: {self.namn}, Tröjnummer: {self.jersey}, År: {self.year}"


class Arena(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    namn = db.Column(db.String(50), unique = False, nullable = False)
    address = db.Column(db.String(100), unique = False, nullable = False)

with app.app_context():
    db.create_all()
    db.session.connection()
    
    while True:
        print("1. Skapa Team")
        print("2. Visa alla teams")
        print("3. Skapa en spelare")
        print("4. Visa alla spelare")
        print("5. Sök efter spelare")
        print("6. Uppdatera")
        print("0. Avsluta")
        
        meny_val = input(">>> ")
        
        match meny_val:
            case "1":
                namn = input("Ange namnet på laget: ")
                stad = input("Ange namnet på staden: ")
                nytt_lag = Team()
                nytt_lag.namn = namn
                nytt_lag.city = stad
                db.session.add(nytt_lag)
                db.session.commit()
            
            case "2":
                for team in Team.query.all():
                    print(team)
                    for player in team.players:
                        print("\t-" + str(player))
                    
            case "3":
                new_spelare = Player()
                new_spelare.namn = input("Ange spelarens namn: ")
                new_spelare.jersey = int(input("Ange nummer på spelarens tröjan: "))
                new_spelare.year = int(input("Ange spelarens år: "))
                
                
                print("Välj ett lag: ")
                for team in Team.query.all():
                    print(f"{team.id}, {team.namn}")
                
                new_spelare.team_id = int(input("Ange team-id: "))
                db.session.add(new_spelare)
                db.session.commit()
                
                
            case "4":
                for player in Player.query.all():
                    print(player)
                
            
            case "5":
                print("A. Sök på tröjnummer")
                print("B. Sök på namn")
                sök = input(">>> ")
                match sök:
                    case "A":
                        tröjnummer = int(input("Ange tröjnummer: "))
                        spelare = Player.query.filter_by(jersey=tröjnummer).all()
                        if spelare:
                            for s in spelare:
                                print(s)
                        
                    case "B":
                        sökord = input("Ange namn: ")
                        spelare = Player.query.filter(Player.namn.contains(sökord)).all()
                        
                        if spelare:
                            for s in spelare:
                                print(s)

            case "6":
                print("a. Team")
                print("b. Player")
                
                uppdatera_val = input(">>> ")
                
                match uppdatera_val:
                    case "a":
                        print(f"|{"ID":>20}|{"NAMN":>20}|")
                        for team in Team.query.all():
                            print(f"|{team.id:>20}|{team.namn:>20}|")
                        
                        upp_team_id = int(input("Ange team-id: "))
                        
                        uppdatera_team:Team = Team.query.filter_by(id=upp_team_id).first()
                        
                        if uppdatera_team:
                            uppdatera_team.namn = input("Ange nytt namn: ")
                            uppdatera_team.city = input("Ange ny stad: ")
                            db.session.add(uppdatera_team)
                            db.session.commit()
                        
                        
                    case "b":
                        ...
            
            case "0":
                break
            
            case _:
                print("Ogiltigt val!")