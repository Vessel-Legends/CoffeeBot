import requests, base64, random, os, hikari, lightbulb
bot = lightbulb.BotApp("")
@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")
@bot.listen(hikari.GuildJoinEvent)
async def on_join(event):
    guild = event.guild_id
    print(f"Bot was added to a server with guild ID: {guild}")

@bot.command
@lightbulb.command("voices", "List of voices available by ID only.",)
@lightbulb.implements(lightbulb.SlashCommand)
async def voiceslist(ctx):
    voicesavail = [
        "[en_au_001] [EN]",
        "[en_au_002] [EN]", 
        "[en_uk_001] [EN]",
        "[en_uk_002] [EN]",
        "[en_us_001] [EN]",
        "[en_female_emotional] [EN]",
        "[es_mx_002] [EN, ES]",
        "[br_001] [EN, PT]",
        "[en_female_madam_leota] [EN]",
        "[en_male_ghosthost] [EN]"]
    await ctx.respond(f"{voicesavail}\n\nMore voices might be added and some might be premium, I havent decided.")
    await ctx.respond("Once you have the ID selected, run **'/tts [text] [speaker]'**")

@bot.command
@lightbulb.option("debuginfo", "Prints debug.", required=False, type=bool)
@lightbulb.option("speaker", "The speaker. MUST BE AN ID! Run '/voices' for the ID.", type=str, required=True, choices=["en_au_001", "en_au_002", "en_uk_001", "en_uk_002", "en_us_001", "en_female_emotional", "es_mx_002", "br_001", "en_female_madam_leota", "en_male_ghosthost"])
@lightbulb.option("text", "The text to generate.", type=str)
@lightbulb.command("tts", "Main TTS stuff.")
@lightbulb.implements(lightbulb.SlashCommand)
async def mainthing(ctx):
    text_speaker = ctx.options.speaker
    req_text = ctx.options.text
    if len(req_text) > 250:
        await ctx.respond(f"You have too many characters! The limit is 250 characters, but you have {len(req_text)} characters.")
        return
    else:
        req_text = ctx.options.text
    filename = "voice" + "-" + str(random.randint(1, 5000)) + ".wav"
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': 'sessionid=f958b30a3fc8aaea5689737429d9bc05'
    }
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers=headers)
    if r.json()["message"] == "Couldn't load speech. Try again.":
        await ctx.respond("Session ID was not correct, or the service is unavailable")
        return
    if r.json()["message"] == "This voice is unavailable now":
        await ctx.respond("Voice ID entered does not exist or was entered incorrectly.")
        return
    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]
    b64d = base64.b64decode(vstr)
    with open(filename, "wb") as out:
        out.write(b64d)
    if ctx.options.debuginfo == True:
        await ctx.respond("Success. Sending audio file plus debug...")
        await ctx.respond(f"Message: {msg}, status_code: {scode}, log: {log}, duration: {dur}, speaker_info: {spkr}")
    else:
        await ctx.respond("Success. Sending audio file...")
    f = hikari.File(filename)
    await ctx.respond(f)
    os.remove(filename)

bot.run(
    activity=hikari.Activity(name=f"Tiktok", type=hikari.ActivityType.WATCHING),
    ignore_session_start_limit=True,
    check_for_updates=False,
    status=hikari.Status.ONLINE,
    coroutine_tracking_depth=20,
    propagate_interrupts=True
)
