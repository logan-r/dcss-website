#!/usr/bin/python

"""Collect dgl-status files from every server, parse them and write 'dgl-status.json'.

Intended to be run every few minutes from cron."""

import json
import sys
import urllib2

if len(sys.argv) != 3:
    print 'error: incorrect number of arguments'
    print 'usage: %s servers.json outfile' % sys.argv[0]
    print 'eg: %s /var/www/servers.json /var/www/dgl-status.json' % sys.argv[0]
    sys.exit(1)

OUTFILE = sys.argv[2]
SERVERS = json.load(open(sys.argv[1], 'r'))

SP_TABLE = {'Mf': 'Merfolk', 'Ke': 'Kenku*', 'MD': 'Mountain Dwarf*', 'Og': 'Ogre', 'Na': 'Naga', 'DD': 'Deep Dwarf', 'DE': 'Deep Elf', 'Tr': 'Troll', 'Mu': 'Mummy', 'GE': 'Grey Elf*', 'VS': 'Vine Stalker', 'HO': 'Hill Orc', 'Sp': 'Spriggan', 'Te': 'Tengu', 'HD': 'Hill Dwarf*', 'HE': 'High Elf', 'El': 'Elf*', 'OM': 'Ogre-Mage*', 'Dj': 'Djinni*', 'Gr': 'Gargoyle', 'Ko': 'Kobold', 'Dg': 'Demigod', 'Gh': 'Ghoul', 'Fo': 'Formicid', 'Ce': 'Centaur', 'Hu': 'Human', 'Vp': 'Vampire', 'Op': 'Octopode', 'Mi': 'Minotaur', 'Pl': 'Plutonian*', 'LO': 'Lava Orc*', 'Gn': 'Gnome*', 'Ha': 'Halfling', 'Dr': 'Draconian', 'Ds': 'Demonspawn', 'SE': 'Sludge Elf*', 'Fe': 'Felid'}
BG_TABLE = {'Pr': 'Priest*', 'CK': 'Chaos Knight', 'AE': 'Air Elementalist', 'DK': 'Death Knight', 'Cj': 'Conjurer', 'EE': 'Earth Elementalist', 'Mo': 'Monk', 'AM': 'Arcane Marksman', 'Ne': 'Necromancer', 'Su': 'Summoner', 'VM': 'Venom Mage', 'Sk': 'Skald', 'Re': 'Reaver*', 'Pa': 'Paladin*', 'FE': 'Fire Elementalist', 'Th': 'Thief*', 'Cr': 'Crusader*', 'St': 'Stalker*', 'IE': 'Ice Elementalist', 'Be': 'Berserker', 'En': 'Enchanter', 'Wn': 'Wanderer', 'Jr': 'Jester*', 'Hu': 'Hunter', 'AK': 'Abyssal Knight', 'As': 'Assassin', 'Ar': 'Artificer', 'Wr': 'Warper', 'Fi': 'Fighter', 'Gl': 'Gladiator', 'Tm': 'Transmuter', 'Wz': 'Wizard', 'He': 'Healer'}
BR_TABLE = {'D': 'Dungeon', 'Orc': 'Orcish Mines', 'Elf': 'Elven Halls', 'Lair': 'Lair of the Beasts', 'Depths': 'Depths', 'Swamp': 'Swamp', 'Shoals': 'Shoals', 'Spider': 'Spider Nest', 'Snake': 'Snake Pit', 'Slime': 'Slime Pits', 'Vaults': 'Vaults', 'Crypt': 'Crypt', 'Tomb': 'Tomb of the Ancients', 'Dis': 'Iron City of Dis', 'Geh': 'Gehenna', 'Coc': 'Cocytus', 'Tar': 'Tartarus', 'Zot':'Realm of Zot', 'Abyss': 'Abyss', 'Zig': 'Ziggurat', 'Lab': 'Labyrinth', 'Bazaar': 'Bazaar', 'WizLab': 'Wizard\'s Laboratory', 'Sewer': 'Sewer', 'Bailey': 'Bailey', 'Ossuary': 'Ossuary', 'IceCv': 'Ice Cave', 'Volcano': 'Volcano', 'Hell': 'Vestibule of Hell', 'Temple': 'Ecumenical Temple', 'Pan': 'Pandemonium', 'Trove': 'Treasure Trove'}

def main():
    dump_games(get_games(SERVERS), OUTFILE)

def parse_location(location):
    """Parse raw location string and return (branch, branchlevel, humanreadable).

    The human readable string is quite complex. There are six forms:
    * On level 1 of the Dungeon/Abyss/...
    * On level 1 of a Ziggurat
    * In a Labyrinth/Wizard Lab/...
    * In an Ice Cave/Ossuary
    * In the Vestibule of Hell/Ecumenical Temple
    * In Pandemonium
    """
    if ':' in location:
        br = location.split(':', 1)[0]
        branchlevel = location.split(':')[1]
    else:
        br = location
        branchlevel = '0'
    branch = BR_TABLE.get(br, br)

    if br in ('D', 'Orc', 'Elf', 'Lair', 'Depths', 'Swamp', 'Shoals', 'Slime', 'Snake', 'Spider', 'Vaults', 'Crypt', 'Tomb', 'Dis', 'Geh', 'Coc', 'Tar', 'Zot', 'Abyss'):
        humanreadable = "on level {} of the {}".format(branchlevel, branch)
    elif br in ('Zig',):
        humanreadable = "on level {} of a {}".format(branchlevel, branch)
    elif br in ('Lab', 'Bazaar', 'WizLab', 'Sewer', 'Bailey', 'Volcano', 'Trove'):
        humanreadable = "in a {}".format(branch)
    elif br in ('Ossuary', 'IceCv'):
        humanreadable = "in an {}".format(branch)
    elif br in ('Hell', 'Temple'):
        humanreadable = "in the {}".format(branch)
    elif br in ('Pan',):
        humanreadable = "in {}".format(branch)
    else:
        humanreadable = 'at {}'.format(location)

    return (branch, branchlevel, humanreadable)

def parse_line(line):
    if not 3 < line.count('#') < 7:
        return None
    split = line.split('#')
    game = {}
    game['name'] = split[0]
    game['rawversion'] = split[1]
    if 'trunk' in split[1] or 'git' in split[1]:
        game['version'] = 'Trunk'
    elif '-' in split[1]:
        game['version'] = split[1].split('-', 1)[1]
    if split[2]: # sometimes this field is blank
        game['XL'] = split[2].split(',')[0].split(' ')[0][1:]
        game['sp'] = split[2].split(' ')[1][:-1][:2]
        game['species'] = SP_TABLE.get(game['sp'], game['sp'])
        game['bg'] = split[2].split(' ')[1][:-1][-2:]
        game['background'] = BG_TABLE.get(game['bg'], game['bg'])
        location = split[2].split(', ')[1]
        game['branch'], game['branchlevel'], game['location'] = parse_location(location)
    if 'x' in split[3]: # sometimes this field is missing
        game['termwidth'], game['termheight'] = split[3].split('x')
        game['idle'] = split[4]
        game['viewers'] = split[5]
    else:
        game['idle'] = split[3]
        game['viewers'] = split[4]

    return game

def get_games(servers):
    games = []

    for server in servers:
        url = server.get('dgl-status')
        if not url:
            continue
        response = urllib2.urlopen(url, timeout=5)
        if response.getcode() != 200:
            print "Warning: %s returned status code %s, skipping." % (url, response.getcode())
        for line in response.read().splitlines():
            try:
                game = parse_line(line)
            except StandardError as e:
                print "Warning: couldn't parse line '%s' from %s." % (line, server['name'])
                continue
            if not game:
                print "Warning: ignoring line '%s' from %s (doesn't have 4-6 # characters)" % (line, url)
                continue
            game['source'] = server['shortname']
            if 'watchurl' in server:
                game['watchurl'] = server['watchurl'].format(name=game['name'])
            games.append(game)

    return games

def dump_games(games, dest):
    # compact dump format
    json.dump(games, open(dest, 'w'), separators=(',', ':'))

if __name__ == '__main__':
    main()
