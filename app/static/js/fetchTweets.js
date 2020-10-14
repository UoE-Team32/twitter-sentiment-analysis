async function query_tweets(search_term, query_limit) {
    try {
        // Disable the search button
        const btn = document.getElementById("search_button");
        btn.disabled = true;

        const res = await axios.get(`/app/piechart?q=${escape(search_term)}&maxResults=${query_limit}`);

        // Re-enable button
        btn.disabled = false;

        return res.data;
    } catch (err) {
        console.error(err);
    }
}
