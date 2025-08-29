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
    'QB': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'POCKET PASSER': 1.15,
            'BACKFIELD CREATOR': 0.75,
            'DUAL THREAT': 1.00,
            'PURE RUNNER': 0.80,
        }
    },
    'HB': {
        'min': 4,
        'ideal': 6,
        'archetypes': {
            'BACKFIELD THREAT': 0.90,
            'CONTACT SEEKER': 0.80,
            'ELUSIVE BRUISER': 1.20,
            'EAST/WEST PLAYMAKER': 1.00,
            'NORTH/SOUTH RECEIVER': 0.80,
            'NORTH/SOUTH BLOCKER': 0.20,
        }
    },
    'FB': {
        'min': 0,
        'ideal': 0,
        'archetypes': {
            'UTILITY': 1.00,
            'BLOCKING': 1.00,
        }
    },
    'WR': {
        'min': 5,
        'ideal': 8,
        'archetypes': {
            'SPEEDSTER': 1.15,
            'CONTESTED SPECIALIST': 1.10,
            'ELUSIVE ROUTE RUNNER': 1.10,
            'PHYSICAL ROUTE RUNNER': 1.00,
            'ROUTE ARTIST': 1.00,
            'GADGET': 0.90,
            'GRITTY POSSESSION': 0.80,
        }
    },
    'TE': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PHYSICAL ROUTE RUNNER': 0.90,
            'PURE BLOCKER': 1.00,
            'VERTICAL THREAT': 1.10,
            'GRITTY POSSESSION': 0.85,
            'PURE POSSESSION': 1.00,
        }
    },
    'LT': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PASS PROTECTOR': 1.10,
            'AGILE': 1.00,
            'WELL ROUNDED': 1.00,
            'RAW STRENGTH': 0.80,
        }
    },
    'LG': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PASS PROTECTOR': 0.90,
            'AGILE': 1.10,
            'WELL ROUNDED': 1.20,
            'RAW STRENGTH': 1.00,
        }
    },
    'C': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PASS PROTECTOR': 0.90,
            'AGILE': 1.10,
            'WELL ROUNDED': 1.20,
            'RAW STRENGTH': 1.00,
        }
    },
    'RG': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PASS PROTECTOR': 0.90,
            'AGILE': 1.10,
            'WELL ROUNDED': 1.20,
            'RAW STRENGTH': 1.00,
        }
    },
    'RT': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'PASS PROTECTOR': 1.10,
            'AGILE': 1.00,
            'WELL ROUNDED': 1.00,
            'RAW STRENGTH': 0.80,
        }
    },
    'LEDG': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'POWER RUSHER': 1.00,
            'SPEED RUSHER': 1.10,
            'EDGE SETTER': 0.90,
            'PURE POWER': 0.90,
        }
    },
    'REDG': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'POWER RUSHER': 1.00,
            'SPEED RUSHER': 1.10,
            'EDGE SETTER': 0.90,
            'PURE POWER': 0.90,
        }
    },
    'DT': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'POWER RUSHER': 1.00,
            'SPEED RUSHER': 0.90,
            'GAP SPECIALIST': 1.10,
            'PURE POWER': 1.00,
        }
    },
    'WILL': {
        'min': 2,
        'ideal': 4,
        'archetypes': {
            'LURKER': 1.10,
            'SIGNAL CALLER': 0.80,
            'THUMPER': 1.00,
        }
    },
    'MIKE': {
        'min': 3,
        'ideal': 4,
        'archetypes': {
            'LURKER': 1.10,
            'SIGNAL CALLER': 0.80,
            'THUMPER': 1.10,
        }
    },
    'SAM': {
        'min': 2,
        'ideal': 4,
        'archetypes': {
            'LURKER': 1.10,
            'SIGNAL CALLER': 0.80,
            'THUMPER': 1.00,
        }
    },
    'CB': {
        'min': 5,
        'ideal': 7,
        'archetypes': {
            'BOUNDARY': 0.95,
            'BUMP AND RUN': 1.05,
            'ZONE': 1.05,
            'FIELD': 1.00,
        }
    },
    'FS': {
        'min': 2,
        'ideal': 3,
        'archetypes': {
            'COVERAGE SPECIALIST': 1.10,
            'HYBRID': 1.10,
            'BOX SPECIALIST': 0.85,
        }
    },
    'SS': {
        'min': 2,
        'ideal': 3,
        'archetypes': {
            'COVERAGE SPECIALIST': 1.10,
            'HYBRID': 0.90,
            'BOX SPECIALIST': 0.85,
        }
    },
    'K': {
        'min': 1,
        'ideal': 1,
        'archetypes': {
            'ACCURATE': 0.90,
            'POWER': 1.00,
        }
    },
    'P': {
        'min': 1,
        'ideal': 1,
        'archetypes': {
            'ACCURATE': 0.90,
            'POWER': 1.00,
        }
    }
}

# Position depth
STARTERS_COUNT = {
    'QB': 1, 'HB': 2, 'FB': 1, 'WR': 3, 'TE': 1,
    'LT': 1, 'LG': 1, 'C': 1, 'RG': 1, 'RT': 1,
    'LEDG': 1, 'REDG': 1, 'DT': 2, 'WILL': 1, 'MLB': 1, 'SAM': 1,
    'CB': 2, 'FS': 1, 'SS': 1, 'K': 1, 'P': 1
}
