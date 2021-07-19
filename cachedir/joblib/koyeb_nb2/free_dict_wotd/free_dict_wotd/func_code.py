# first line: 18
@memory.cache
def free_dict_wotd(day: float = 0):
    """Fetch wotd and idiom of the day from freedictionayr.com.

    day: time() // (24 * 3600), cached for the same day, will not visit the website to fetch info.
    """
    try:
        day = int(day)
    except Exception:
        day = 0

    url = "https://www.thefreedictionary.com/"
    try:
        resp = httpx.get(url, verify=False, timeout=30)
        # resp = requests.get(url, verify=False, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return str(exc), ""

    # '#Content_CA_WOD_0_DataZone'
    doc = pq(resp.content)
    wotd = doc("#Content_CA_WOD_0_DataZone")
    wotd = wotd.make_links_absolute(url)
    wotd_str = wotd.text().replace(":\n", ": ")

    links = wotd("a")
    wotd_href = links[0].attrib.get("href")
    if isinstance(wotd_href, str):
        wotd_str = wotd_str.replace("Discuss.", wotd_href)

    # idiom of the day
    selector = "#Content_CA_IOD_0_trDz"
    iotd = doc(selector)
    # more_link
    # sel = '#Content_CA_IOD_0_DataZone > a:nth-child(3)'
    iotd = iotd.make_links_absolute(url)
    # more = iotd(sel)
    text = iotd("span").text()
    # list of <Element a at 0x25377944318>: links[0].text, links[0].attrib['href']
    links = iotd("a")

    link = links[0]
    details = ["{}".format(link.text)]
    details += [text] + [" ({}) ".format(link.attrib["href"])]
    for link in links[1:]:
        # link = pq(link)
        details += ["{} ({}) ".format(link.text, link.attrib["href"])]
    iotd_str = "\n".join(details)
    return wotd_str, iotd_str
