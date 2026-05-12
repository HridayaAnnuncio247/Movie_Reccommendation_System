from movie import Movie

m = Movie()

year_range = [2016, 2026]

language = "en"#"Hindi"

API_KEY = "96e28253d91e3dfe2b7e5a61c83fc998"




m.run_api(year_range, language, API_KEY)