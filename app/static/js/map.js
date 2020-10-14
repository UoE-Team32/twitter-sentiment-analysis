var app = new Vue({
  el: "#app",
  delimiters: ['[[', ']]'],
  data: {
      search_term: "",
      query_limit: 100,
      data: [1, 1, 1],
      overallPieChart: null,
      isLoading: false,
      tweets: null,
      center: { lat: 41.90476224706472, lng: 12.49822074385094 },
      zoom: 14,
      url: "https://maps.googleapis.com/maps/api/staticmap",
  },
  methods: {
    async query() {
      // Set loading to opposite of itself
      this.isLoading = !this.isLoading;
      const loader = new google.maps.plugins.loader.Loader({
        apiKey: "AIzaSyDlX9P57vFkRLB-qCDX6zb_dvHpTDsUBjU",
        version: "weekly",
      });

      // Fetch the tweets based on the query
      await query_tweets(this.search_term, this.query_limit).then((data) => {
        this.tweets = data;
        center = this.center
        zoom = this.zoom
        
        wrapper.remove();
        loader.load().then(() => {
          map = new google.maps.Map(document.getElementById("map"), {
            center,
            zoom,
          });
        });
      }).catch((err) => {
        console.error(err);
      });
    },
  },
  mounted() {
    let map;
    document.addEventListener("DOMContentLoaded", () => {
      const wrapper = document.getElementById("wrapper");
      wrapper.style.backgroundImage = `url(${this.url}?center=${this.center.lat},${this.center.lng}&zoom=${this.zoom}&scale=2&size=${wrapper.clientWidth}x${wrapper.clientHeight}&key=AIzaSyDlX9P57vFkRLB-qCDX6zb_dvHpTDsUBjU)`;
      console.log(`url(${this.url}?center=${this.center.lat},${this.center.lng}&zoom=${this.zoom}&scale=2&size=${wrapper.clientWidth}x${wrapper.clientHeight}&key=AIzaSyDlX9P57vFkRLB-qCDX6zb_dvHpTDsUBjU)`)    
    });
  }
});
