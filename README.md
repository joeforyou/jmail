# jmail

This is a simple Python email program that sends an email with a random Jeopardy question using [jService](http://jservice.io/). Users are meant to open the email and record their win or loss in Google Sheets. 

## Formulas for Google Sheets

Total for Player 1:
`=sum('3'!C:C, '4'!C:C, '5'!C:C, '6'!C:C, '7'!C:C, '8'!C:C,'9'!C:C, '10'!C:C, '11'!C:C,'12'!C:C)`

Total for Player 2:
`=sum('3'!B:B, '4'!B:B, '5'!B:B, '6'!B:B, '7'!B:B, '8'!B:B,'9'!B:B, '10'!B:B, '11'!B:B,'12'!B:B)`
