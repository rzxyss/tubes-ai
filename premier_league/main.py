import pandas as pd

logo = {
    'nama_tim' : [
        'Liverpool',
        'Arsenal',
        'Nottingham Forest',
        'Chelsea',
        'Newcastle United',
        'Manchester City',
        'AFC Bournemouth',
        'Fulham',
        'Aston Villa',
        'Brighton & Hove Albion',
        'Tottenham Hotspur',
        'Brentford',
        'West Ham United',
        'Manchester United',
        'Crystal Palace',
        'Everton',
        'Wolverhampton Wanderers',
        'Ipswich Town',
        'Leicester City',
        'Southampton'
    ],
    'logo': [
        'assets/Liverpool.png',
        'assets/Arsenal.png',
        'assets/Nottingham Forest.png',
        'assets/Chelsea.png',
        'assets/Newcastle United.png',
        'assets/Manchester City.png',
        'assets/AFC Bournemouth.png',
        'assets/Fulham.png',
        'assets/Aston Villa.png',
        'assets/Brighton & Hove Albion.png',
        'assets/Tottenham Hotspur.png',
        'assets/Brentford.png',
        'assets/West Ham United.png',
        'assets/Manchester United.png',
        'assets/Crystal Palace.png',
        'assets/Everton.png',
        'assets/Wolverhampton Wanderers.png',
        'assets/Ipswich Town.png',
        'assets/Leicester City.png',
        'assets/Southampton.png'
    ]
}

df = pd.DataFrame(logo)
df.to_csv('logo_tim.csv', index=False)