from bs4 import BeautifulSoup

XML = '''
    <edom>
    <edomv>01</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>02</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>03</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>04</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>05</edomv>
    <edomvd>VACANT AGRICULTURAL</edomvd>
    </edom>
    <edom>
    <edomv>06</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>07</edomv>
    <edomvd>VACANT LAND</edomvd>
    </edom>
    <edom>
    <edomv>10</edomv>
    <edomvd>CONDOMINIUMS</edomvd>
    </edom>
    <edom>
    <edomv>11</edomv>
    <edomvd>SINGLE FAMILY RESIDENTIAL</edomvd>
    </edom>
    <edom>
    <edomv>12</edomv>
    <edomvd>DUPLEX</edomvd>
    </edom>
    <edom>
    <edomv>13</edomv>
    <edomvd>TRIPLEX</edomvd>
    </edom>
    <edom>
    <edomv>14</edomv>
    <edomvd>APARTMENT - 4 UNITS</edomvd>
    </edom>
    <edom>
    <edomv>15</edomv>
    <edomvd>APARTMENT - 5 UNITS</edomvd>
    </edom>
    <edom>
    <edomv>16</edomv>
    <edomvd>APARTMENT - 6 UNITS</edomvd>
    </edom>
    <edom>
    <edomv>17</edomv>
    <edomvd>APARTMENT - 7 UNITS</edomvd>
    </edom>
    <edom>
    <edomv>18</edomv>
    <edomvd>APARTMENT 8 UNITS</edomvd>
    </edom>
    <edom>
    <edomv>19</edomv>
    <edomvd>ROWHOUSE/TOWNHOME</edomvd>
    </edom>
    <edom>
    <edomv>20</edomv>
    <edomvd>APARTMENT - 9+ UNITS</edomvd>
    </edom>
    <edom>
    <edomv>21</edomv>
    <edomvd>PLANED BUILDING GROUP - APARTMENT</edomvd>
    </edom>
    <edom>
    <edomv>22</edomv>
    <edomvd>HOTEL</edomvd>
    </edom>
    <edom>
    <edomv>23</edomv>
    <edomvd>MOTEL</edomvd>
    </edom>
    <edom>
    <edomv>24</edomv>
    <edomvd>RETAIL</edomvd>
    </edom>
    <edom>
    <edomv>25</edomv>
    <edomvd>RESTAURANT</edomvd>
    </edom>
    <edom>
    <edomv>26</edomv>
    <edomvd>SHOPPING CENTER</edomvd>
    </edom>
    <edom>
    <edomv>27</edomv>
    <edomvd>THEATRE</edomvd>
    </edom>
    <edom>
    <edomv>28</edomv>
    <edomvd>MISCELLANEOUS COMMERCIAL IMPROVEMENTS</edomvd>
    </edom>
    <edom>
    <edomv>29</edomv>
    <edomvd>COMMERCIAL PARKING STRUCTURE</edomvd>
    </edom>
    <edom>
    <edomv>30</edomv>
    <edomvd>OFFICES</edomvd>
    </edom>
    <edom>
    <edomv>31</edomv>
    <edomvd>FINANCIAL BUILDINGS</edomvd>
    </edom>
    <edom>
    <edomv>32</edomv>
    <edomvd>MEDICAL</edomvd>
    </edom>
    <edom>
    <edomv>33</edomv>
    <edomvd>SOCIAL/RECREATION</edomvd>
    </edom>
    <edom>
    <edomv>35</edomv>
    <edomvd>VETERINARIES</edomvd>
    </edom>
    <edom>
    <edomv>36</edomv>
    <edomvd>MORTUARIES</edomvd>
    </edom>
    <edom>
    <edomv>37</edomv>
    <edomvd>CEMETERY BUILDINGS</edomvd>
    </edom>
    <edom>
    <edomv>39</edomv>
    <edomvd>GOVERNMENTAL BUILDING</edomvd>
    </edom>
    <edom>
    <edomv>40</edomv>
    <edomvd>GREENHOUSE</edomvd>
    </edom>
    <edom>
    <edomv>41</edomv>
    <edomvd>GRAIN ELEVATOR</edomvd>
    </edom>
    <edom>
    <edomv>42</edomv>
    <edomvd>DRY CLEANING PLANT</edomvd>
    </edom>
    <edom>
    <edomv>43</edomv>
    <edomvd>PRINTING PLANT</edomvd>
    </edom>
    <edom>
    <edomv>44</edomv>
    <edomvd>WAREHOUSE</edomvd>
    </edom>
    <edom>
    <edomv>45</edomv>
    <edomvd>MEAT PACKING</edomvd>
    </edom>
    <edom>
    <edomv>46</edomv>
    <edomvd>FOOD PROCESSING</edomvd>
    </edom>
    <edom>
    <edomv>47</edomv>
    <edomvd>FACTORY</edomvd>
    </edom>
    <edom>
    <edomv>48</edomv>
    <edomvd>BRICK PLANT</edomvd>
    </edom>
    <edom>
    <edomv>50</edomv>
    <edomvd>AIRPORT TAXABLE</edomvd>
    </edom>
    <edom>
    <edomv>51</edomv>
    <edomvd>RAILROAD OWNED TAXABLE</edomvd>
    </edom>
    <edom>
    <edomv>52</edomv>
    <edomvd>AUTO SHIPPING OR TRUCKING TERMINAL</edomvd>
    </edom>
    <edom>
    <edomv>53</edomv>
    <edomvd>SERVICE STATION</edomvd>
    </edom>
    <edom>
    <edomv>54</edomv>
    <edomvd>CAR WASH</edomvd>
    </edom>
    <edom>
    <edomv>55</edomv>
    <edomvd>AUTO DEALER</edomvd>
    </edom>
    <edom>
    <edomv>56</edomv>
    <edomvd>
    PARKING BUILDING - NOT ASSOCIATED WITH COMMERCIAL USEAGE
    </edomvd>
    </edom>
    <edom>
    <edomv>57</edomv>
    <edomvd>AUTO SERVICE</edomvd>
    </edom>
    <edom>
    <edomv>58</edomv>
    <edomvd>MISCELLANEOUS INDUSTRIAL IMPROVEMENTS</edomvd>
    </edom>
    <edom>
    <edomv>60</edomv>
    <edomvd>MOBILE HOMES</edomvd>
    </edom>
    <edom>
    <edomv>61</edomv>
    <edomvd>MOBILE HOME PARK</edomvd>
    </edom>
    <edom>
    <edomv>80</edomv>
    <edomvd>CITY LEASED BUILDING</edomvd>
    </edom>
    <edom>
    <edomv>81</edomv>
    <edomvd>AIRPORTS</edomvd>
    </edom>
    <edom>
    <edomv>82</edomv>
    <edomvd>CITY & COUNTY OF DENVER</edomvd>
    </edom>
    <edom>
    <edomv>83</edomv>
    <edomvd>DENVER HOUSING</edomvd>
    </edom>
    <edom>
    <edomv>84</edomv>
    <edomvd>SENIOR CITIZENS HOMES</edomvd>
    </edom>
    <edom>
    <edomv>85</edomv>
    <edomvd>UNITED STATES GOVERMENT</edomvd>
    </edom>
    <edom>
    <edomv>86</edomv>
    <edomvd>STATE OF COLORADO</edomvd>
    </edom>
    <edom>
    <edomv>87</edomv>
    <edomvd>LOWRY OR GEORGE W CLAYTON TRUST ESTATE</edomvd>
    </edom>
    <edom>
    <edomv>88</edomv>
    <edomvd>COLORADO SEMINARY</edomvd>
    </edom>
    <edom>
    <edomv>89</edomv>
    <edomvd>DENVER PUBLIC SCHOOLS</edomvd>
    </edom>
    <edom>
    <edomv>90</edomv>
    <edomvd>PRIVATE SCHOOLS</edomvd>
    </edom>
    <edom>
    <edomv>91</edomv>
    <edomvd>PAROCHIAL SCHOOLS</edomvd>
    </edom>
    <edom>
    <edomv>92</edomv>
    <edomvd>CHURCH/RELIGEOUS WORSHIP</edomvd>
    </edom>
    <edom>
    <edomv>93</edomv>
    <edomvd>HOSPITAL</edomvd>
    </edom>
    <edom>
    <edomv>94</edomv>
    <edomvd>FRATERNAL</edomvd>
    </edom>
    <edom>
    <edomv>95</edomv>
    <edomvd>ALL OTHER CHARITABLE EXEMPTS</edomvd>
    </edom>
    <edom>
    <edomv>96</edomv>
    <edomvd>ALL OTHER EXEMPT</edomvd>
    </edom>
    <edom>
    <edomv>97</edomv>
    <edomvd>PARSONAGES</edomvd>
    </edom>
    <edom>
    <edomv>98</edomv>
    <edomvd>STATE ASSESSED</edomvd>
    </edom>
    <edom>
    <edomv>99</edomv>
    <edomvd>GENERAL COMMON ELEMENTS</edomvd>
    </edom>
    '''

def original_use_ids():
    soup = BeautifulSoup(XML, 'html.parser')
    xml_pairs = soup.find_all('edom')
    cleaned_data = []
    for xml_tag in xml_pairs:
        pair = xml_tag.findChildren()
        text_data = [_.text.encode('utf-8') for _ in pair]
        cleaned_pair = tuple([int(text_data[0]), text_data[1].strip('\n ')])
        cleaned_data.append(cleaned_pair)
    return cleaned_data

def unique_use_ids():
    soup = BeautifulSoup(XML, 'html.parser')
    xml_pairs = soup.find_all('edom')
    cleaned_data = []
    for xml_tag in xml_pairs:
        pair = xml_tag.findChildren()
        text_data = [_.text.encode('utf-8') for _ in pair]
        cleaned_pair = text_data[1].strip('\n ')
        cleaned_data.append(cleaned_pair)

    cleaned_data = sorted(list(set(cleaned_data)))
    cleaned_data = [tuple([i, datum]) for i, datum in enumerate(cleaned_data, start=1)]
    return cleaned_data

if __name__ == '__main__':
    l = unique_use_ids()
    for _ in l:
        print _,','
