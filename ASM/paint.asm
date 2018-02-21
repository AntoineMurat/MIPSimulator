init:
and $2, $0, $0
and $6, $0, $0
and $9, $0, $0
and $14, $0, $0
and $24, $0, $0
and $22, $0, $0
and $3, $0, $0
and $4, $0, $0

ori $2, $0, 0xF0F0 # $2 <- Couleur
ori $6, $0, 0x140 # $6 <- Width
ori $9, $0, 0x4004 # bouton
ori $14, $0, 0x4 # $14 <- 4
lui $24, 0xC # $24 <- derniere adresse d'écran
ori $24, $24, 0xAFFF
lui $22, 0x8 # $22 <- debut ecran
debut_boucle: # $3 <- x, $4 <- y
lw $15, 0x0($9) # On charge les boutons
beq $15, $0, slow_speed # si les boutons sont pas activés on skip
high_speed:
addiu $3, $3, 0x1 # On incrémente x
addiu $4, $4, 0x2 # On incrémente y
j fin_increment
slow_speed:
addiu $3, $3, 0x1 # On incrémente x
addiu $4, $4, 0x1 # On incrémente y
j fin_increment
fin_increment:
multu $6, $4 # On passe les lignes
mflo $7
addu $5, $3, $7 # $7 <- Adresse de dessin
multu $14, $5 # On multiplie par 4
mflo $5
addu $5, $5, $22 <- Adresse de dessin
subu $23, $24, $5
bltz $23, init
sw $2, 0x0($5) # On écrit à la bonne place
j debut_boucle
fin:
j fin
