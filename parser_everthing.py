#! /usr/bin/env python


def parser(filepath):
    # get ip , jumplog , ua
    parser_lst = []
    with open(filepath, 'r') as f:
        for line in f:
            if 'ip parser cost:' in line or 'save JumpLog cost:' in line or 'ua parser cost:' in line:
                parser_lst.append(line.strip())
    # continue filter
    ip_ua_jump_lst = []
    for p in parser_lst :
        if 'ip parser cost:' in p or 'save JumpLog cost:' in p:
            p = p.split('-')[-1].strip()
        if 'ua parser cost' in p:
            p = p.split('-')[3].strip()
            p = p[:p.find('[')].strip()
        ip_ua_jump_lst.append(p)


    ip_lst = []
    ua_lst = []
    jump_lst = []

    for line in ip_ua_jump_lst:
        line = line.strip()
        if '.' in line or ',' in line :
            line = line.strip(',').strip('.')
        split_line = line.split(':')
        key, value = split_line[0], split_line[1]
        if key == 'ip parser cost':
            ip_lst.append((key, value))
        elif key == 'save JumpLog cost':
            jump_lst.append((key, value))
        else:
            ua_lst.append((key, value))

    print '***********************************IP PARSER*******************************************************'
    ip_map = {}
    for ip_name, ip_cost in ip_lst:
        if ip_cost not in ip_map:
            ip_map[ip_cost] = 1
        else:
            ip_map[ip_cost] += 1

    keys = ip_map.keys()
    keys = sorted(keys, key = lambda x:int(x.strip('ms')))
    for key in keys:
        value = ip_map[key]
        percent = '{0}%'.format(round(value / 1331721.0, 4) * 100)
        print key, ip_map[key], percent

    print '***********************************UA PARSER*******************************************************'
    ua_map = {}
    for ua_name, ua_cost in ua_lst:
        if ua_cost not in ua_map:
            ua_map[ua_cost] = 1
        else:
            ua_map[ua_cost] += 1

    keys = ua_map.keys()
    keys = sorted(keys, key = lambda x:int(x.strip('ms')))
    for key in keys:
        value = ua_map[key]
        percent = '{0}%'.format(round(value / 1331710.0, 4) * 100)
        print key, value, percent

    print '***********************************SAVE JUMPLOG*******************************************************'
    jump_map = {}
    for jump_name, jump_cost in jump_lst:
        if jump_cost not in jump_map:
            jump_map[jump_cost] = 1
        else:
            jump_map[jump_cost] += 1

    keys = jump_map.keys()
    keys = sorted(keys, key = lambda x:int(x.strip('ms')))
    for key in keys:
        value = jump_map[key]
        percent = '{0}%'.format(round(value / 1331710.0, 4) * 100)
        print key, value, percent




if __name__ == '__main__':
    parser('ymconv.log')

