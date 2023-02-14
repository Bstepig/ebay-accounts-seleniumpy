def store_result(proxy_res, profile_dir, profile):
    results = []
    results.append(f'Proxy:           {proxy_res["proxy"]}')
    results.append(f'Proxy IP:        {proxy_res["out_ip"]}')
    results.append(f'Proxy City:      {proxy_res["city"]}')
    results.append(f'Email:           {profile.get_email()}')
    results.append(f'Email Password:  {profile.email_password}')
    results.append(f'eBay Password:   {profile.ebay_password}')

    file = open(profile_dir + '/result.txt', 'w', encoding='utf8')
    file.write('\n'.join(results))
    file.close()