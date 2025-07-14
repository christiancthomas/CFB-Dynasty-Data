# PLAYER VALUATION
DEV_TRAIT_MULTIPLIERS = {
    'NORMAL': 1.00,
    'IMPACT': 1.10,
    'STAR': 1.25,
    'ELITE': 1.50
}

REMAINING_YEARS = {
    'FR': 3, 'SO': 2, 'JR': 1, 'SR': 0,
    'FR (RS)': 3, 'SO (RS)': 2, 'JR (RS)': 1, 'SR (RS)': 0
}

# Redshirt discount and starter counts
RS_DISCOUNT = 0.05

# Define minimum and ideal roster sizes per position
# TODO: Update positions and archetypes for CFB 26
# TODO: CONFIRM ARCHETYPE VALUATIONS
DEFAULT_POSITION_REQUIREMENTS = {
    'QB': {'min': 3, 'ideal': 4, 'archetypes': {'POCKET PASSER': 1, 'BACKFIELD CREATOR': 0.75, 'DUAL THREAT': 0.75, 'PURE RUNNER': 0.5}},
    'HB': {'min': 4, 'ideal': 6, 'archetypes': {'BACKFIELD THREAT': 0.75, 'CONTACT SEEKER': 0.75, 'ELUSIVE BRUISER': 0.75, 'EAST/WEST PLAYMAKER': 0.75, 'NORTH/SOUTH RECEIVER': 0.5, 'NORTH/SOUTH BLOCKER': 0.2}},
    'FB': {'min': 0, 'ideal': 0, 'archetypes': {'UTILITY': 0, 'BLOCKING': 0}},
    'WR': {'min': 6, 'ideal': 8, 'archetypes': {'CONTESTED SPECIALIST': 0.75, 'ELUSIVE ROUTE RUNNER': 0.75, 'GRITTY POSSESSION': 0.75, 'PHYSICAL ROUTE RUNNER': 0.75, 'ROUTE ARTIST': 0.75, 'SPEEDSTER': 0.75, 'GADGET': 0.5}},
    'TE': {'min': 3, 'ideal': 4, 'archetypes': {'PHYSICAL ROUTE RUNNER': 0.75, 'VERTICAL THREAT': 0.75, 'GRITTY POSSESSION': 0.5, 'POSSESSION': 0.5, 'PURE BLOCKER': 0.25}},
    'LT': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 1, 'AGILE': 0.8, 'WELL ROUNDED': 0.75, 'RAW STRENGTH': 0.6}},
    'LG': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.6, 'AGILE': 1, 'WELL ROUNDED': 0.75, 'RAW STRENGTH': 1}},
    'C':  {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.5, 'AGILE': 1, 'WELL ROUNDED': 0.75, 'RAW STRENGTH': 1}},
    'RG': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.6, 'AGILE': 1, 'WELL ROUNDED': 0.75, 'RAW STRENGTH': 1}},
    'RT': {'min': 3, 'ideal': 4, 'archetypes': {'PASS PROTECTOR': 0.8, 'AGILE': 0.8, 'WELL ROUNDED': 0.75, 'RAW STRENGTH': 0.75}},
    'LEDG': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 0.9, 'EDGE SETTER': 1}},
    'REDG': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 1, 'EDGE SETTER': 1, 'PURE POWER': 0.5}},
    'DT': {'min': 3, 'ideal': 4, 'archetypes': {'POWER RUSHER': 0.9, 'SPEED RUSHER': 0.8, 'GAP SPECIALIST': 1, 'PURE POWER': 0.5}},
    'WILL': {'min': 3, 'ideal': 4, 'archetypes': {'LURKER': 1, 'SIGNAL CALLER': 0.8, 'THUMPER': 1}},
    'MIKE': {'min': 3, 'ideal': 4, 'archetypes': {'LURKER': 0.8, 'SIGNAL CALLER': 1, 'THUMPER': 0.8}},
    'SAM': {'min': 3, 'ideal': 4, 'archetypes': {'LURKER': 1, 'SIGNAL CALLER': 0.8, 'THUMPER': 1}},
    'CB': {'min': 5, 'ideal': 7, 'archetypes': {'BOUNDARY': 1, 'BUMP AND RUN': 1, 'ZONE': 1, 'FIELD': 1}},
    'FS': {'min': 2, 'ideal': 3, 'archetypes': {'COVERAGE SPECIALIST': 1, 'HYBRID': 0.75, 'BOX SPECIALIST': 0.5}},
    'SS': {'min': 2, 'ideal': 3, 'archetypes': {'COVERAGE SPECIALIST': 0.75, 'HYBRID': 0.1, 'BOX SPECIALIST': 0.8}},
    'K': {'min': 1, 'ideal': 1, 'archetypes': {'ACCURATE': 0.75, 'POWER': 1}},
    'P': {'min': 1, 'ideal': 1, 'archetypes': {'ACCURATE': 0.75, 'POWER': 1}}
}

# Position depth
STARTERS_COUNT = {
    'QB': 1, 'HB': 2, 'FB': 1, 'WR': 3, 'TE': 1,
    'LT': 1, 'LG': 1, 'C': 1, 'RG': 1, 'RT': 1,
    'LEDG': 1, 'REDG': 1, 'DT': 2, 'WILL': 1, 'MLB': 1, 'SAM': 1,
    'CB': 2, 'FS': 1, 'SS': 1, 'K': 1, 'P': 1
}