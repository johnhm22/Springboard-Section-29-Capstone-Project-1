


$("#fixtures").on("click", async function getFixtures(){


url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/2790/next/5"

headers = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
response = requests.request("GET", url, headers=headers)

    $(`<p>Your birth year ${resp.data.number} fact is ${resp.data.text}.</p>`).appendTo("#lucky-results");
});
