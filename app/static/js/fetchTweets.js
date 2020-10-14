async function query_tweets(search_term, query_limit, location_required=false) {
    try {
        // Disable the search button
        const btn = document.getElementById("search_button");
        btn.disabled = true;
        var res;
        if (location_required) {
            res = await axios.get(`/app/piechart?q=${escape(search_term)}&maxResults=${query_limit}&locationRequired`);
        } else {
            res = await axios.get(`/app/piechart?q=${escape(search_term)}&maxResults=${query_limit}`);
        }

        // Re-enable button
        btn.disabled = false;

        return res.data;
    } catch (err) {
        console.error(err);
    }
}
