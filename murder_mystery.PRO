domains
name,occupation,dist,character,vice,weapon=symbol
age,shoe_size=integer

predicates
person(name,age,shoe_size,occupation,character)
motive(vice)
has_affair(name,name)
owns_weapon(name,weapon)
blackmails(name,name)
killed(name)
killer(name)
suspect(name)
married_with(name,name)
killed_with(weapon)
distance_fired(dist)
probably_atcrime(name,dist)
footstep_atcrime(shoe_size,dist)

Clauses
person(alexander,50,8,banker,wise).
person(arthur,25,8,none,gambler).
person(mary,23,7,hwife,beautiful).
person(steven,35,10,banker,greedy).
person(lucy,25,7,maid,poor).
person(ed,28,10,butcher,hardworking).
person(george,25,8,businessman,greedy). 

killed(arthur).
killed_with(pistol).
distance_fired(far).

married_with(arthur,mary).

has_affair(arthur,lucy).
has_affair(mary,steven).
has_affair(ed,lucy).

blackmails(george,arthur).

motive(jealousy).
motive(money).
motive(hate).

suspect(X):-
motive(money),
person(X,_,_,_,poor),
write("motive is money ").

suspect(X):-
motive(money),
person(X,_,_,_,greedy),
write("motive is money ").

suspect(X):-
motive(money),
blackmails(X,Y),
killed(Y),
write("motive is blackmail ").

suspect(Y):-
motive(hate),
married_with(X,Y),
has_affair(X,_),
killed(X),
write("motive is hate ").

suspect(X):-
killed(Y),
has_affair(X,Z),
has_affair(Y,Z),
Y<>X,
write("motive is jealousy ").

owns_weapon(ed,knife).
owns_weapon(arthur,pistol).
owns_weapon(steven,pistol).
owns_weapon(george,pistol).

footstep_atcrime(8,near).
footstep_atcrime(10,far).

probably_atcrime(X,Y):-
person(X,_,Z,_,_),
footstep_atcrime(Z,Y),
killed(P),
X<>P.

killer(X):-
killed_with(Y),
distance_fired(Z),
person(X,_,_,_,_),
owns_weapon(X,Y),
probably_atcrime(X,Z).

