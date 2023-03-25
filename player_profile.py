def build_profile(first, last, **player_info):
    """create a dictionary"""
    profile = {}
    profile['first_name'] = first
    profile['last_name'] = last
    for key, value in player_info.items():
        profile[key] = value
    return profile


player_profile = build_profile('Harry', 'Kane', location='London', field='CF')

print(player_profile)
