from hashlib import md5

class Player:
    """
    Represents a player in the CFB Dynasty Data system.
    Players have attributes such as first & last name, position, team, year, and redshirt status.
    """
    def __init__(self, first_name: str, last_name: str, position: str, year: str, overall: str = 0, base_overall: str = 0,
                 city: str = "", state: str = "", archetype: str = "", dev_trait: str = "", cut: bool = False,
                 drafted: str = "", redshirt: bool = False, value: float = 0.0, status: str = "", team: str = "",
                 national_rank: str = "", stars: str = "", gem_status: str = "", committed_to: str = "",
                 transfer: bool = False, transfer_out: bool = False):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.year = year
        self.overall = overall
        self.base_overall = base_overall
        self.city = city
        self.state = state
        self.archetype = archetype
        self.dev_trait = dev_trait
        self.cut = cut
        self.drafted = drafted
        self.redshirt = redshirt
        self.value = value
        self.status = status
        self.team = team
        self.national_rank = national_rank
        self.stars = stars
        self.gem_status = gem_status
        self.committed_to = committed_to
        self.transfer = transfer
        self.transfer_out = transfer_out

        # Generate a unique ID based on player attributes, ignoring case and spaces
        id_vars = f"{first_name}{last_name}{position}{city}{state}".lower().replace(" ", "")
        self.player_id = md5(id_vars.encode()).hexdigest()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position} ({self.year})"

    def to_dict(self) -> dict:
        """
        Convert the player object to a dictionary representation.

        Returns:
            dict: Dictionary containing player attributes.
        """
        return {
            'id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'team': self.team,
            'position': self.position,
            'year': self.year,
            'overall': self.overall,
            'base_overall': self.base_overall,
            'city': self.city,
            'state': self.state,
            'archetype': self.archetype,
            'dev_trait': self.dev_trait,
            'cut': self.cut,
            'drafted': self.drafted,
            'redshirt': self.redshirt,
            'value': self.value,
            'status': self.status,
            'national_rank': self.national_rank,
            'stars': self.stars,
            'gem_status': self.gem_status,
            'committed_to': self.committed_to,
            'transfer': self.transfer,
            'transfer_out': self.transfer_out,
        }

    @classmethod
    def from_dict(cls, player_data: dict):
        """
        Create a Player instance from a dictionary representation.

        Args:
            player_data (dict): Dictionary containing player attributes.

        Returns:
            Player: An instance of the Player class.
        """
        return cls(
            first_name=player_data['first_name'],
            last_name=player_data['last_name'],
            position=player_data['position'],
            year=player_data['year'],
            overall=player_data.get('overall', ''),
            base_overall=player_data.get('base_overall', ''),
            city=player_data.get('city', ''),
            state=player_data.get('state', ''),
            archetype=player_data.get('archetype', ''),
            dev_trait=player_data.get('dev_trait', ''),
            cut=player_data.get('cut', False),
            drafted=player_data.get('drafted', ''),
            redshirt=player_data.get('redshirt', False),
            value=player_data.get('value', ''),
            status=player_data.get('status', ''),
            team=player_data.get('team', ''),
            national_rank=player_data.get('national_rank', ''),
            stars=player_data.get('stars', ''),
            gem_status=player_data.get('gem_status', ''),
            committed_to=player_data.get('committed_to', ''),
            transfer=player_data.get('transfer', False),
            transfer_out=player_data.get('transfer_out', False),
            )

    def advance_year(self):
        """
        Advance the player's year based on their current year and redshirt status.

        If the player is redshirted, they will advance to the next year without changing their status.
        """
        year_mapping = {
            'HS': 'FR',
            'FR': 'SO',
            'SO': 'JR',
            'JR': 'SR',
            'SR': 'GRADUATED',
            'FR (RS)': 'SO (RS)',
            'SO (RS)': 'JR (RS)',
            'JR (RS)': 'SR (RS)',
            'SR (RS)': 'GRADUATED'
            }

        if self.redshirt and 'RS' not in self.year:
            self.year += " (RS)"
        else:
            self.year = year_mapping.get(self.year, self.year)

        return self.year
