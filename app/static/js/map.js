var app = new Vue({
  el: "#app",
  delimiters: ['[[', ']]'],
  data: {
      search_term: "",
      query_limit: 100,
      overallPieChart: null,
      isLoading: false,
      tweets: null,
      wrapper: null,
      center: { lat: 51.8763, lng: 0.9449 },
      zoom: 15,
      url: "https://maps.googleapis.com/maps/api/staticmap",
      locations: [
        { lat: -31.56391, lng: 147.154312 },
        { lat: -33.718234, lng: 150.363181 },
        { lat: -33.727111, lng: 150.371124 },
        { lat: -33.848588, lng: 151.209834 },
        { lat: -33.851702, lng: 151.216968 },
        { lat: -34.671264, lng: 150.863657 },
        { lat: -35.304724, lng: 148.662905 },
        { lat: -36.817685, lng: 175.699196 },
        { lat: -36.828611, lng: 175.790222 },
        { lat: -37.75, lng: 145.116667 },
        { lat: -37.759859, lng: 145.128708 },
        { lat: -37.765015, lng: 145.133858 },
        { lat: -37.770104, lng: 145.143299 },
        { lat: -37.7737, lng: 145.145187 },
        { lat: -37.774785, lng: 145.137978 },
        { lat: -37.819616, lng: 144.968119 },
        { lat: -38.330766, lng: 144.695692 },
        { lat: -39.927193, lng: 175.053218 },
        { lat: -41.330162, lng: 174.865694 },
        { lat: -42.734358, lng: 147.439506 },
        { lat: -42.734358, lng: 147.501315 },
        { lat: -42.735258, lng: 147.438 },
        { lat: -43.999792, lng: 170.463352 },
      ]
  },
  methods: {
    async query() {
      // Set loading to opposite of itself
      this.isLoading = !this.isLoading;
      const loader = new google.maps.plugins.loader.Loader({
        apiKey: GOOGLE_MAPS_API_KEY,
        version: "weekly",
      });

      // Fetch the tweets based on the query
      await query_tweets(this.search_term, this.query_limit, true).then((data) => {
        this.tweets = data;
        console.log(this.tweets.positive)
        center = this.center
        zoom = this.zoom
        if (this.wrapper) {
          this.wrapper.remove();
        }
        loader.load().then(() => {
          map = new google.maps.Map(document.getElementById("map"), {
            center,
            zoom,
          });
          // Create an array of alphabetical characters used to label the markers.
          const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
          // Add some markers to the map.
          // Note: The code uses the JavaScript Array.prototype.map() method to
          // create an array of markers based on a given "locations" array.
          // The map() method here has nothing to do with the Google Maps API.
          const markers = this.locations.map((location, i) => {
            return new google.maps.Marker({
              position: location,
              label: labels[i % labels.length],
            });
          });
          // Add a marker clusterer to manage the markers.
          new MarkerClusterer(map, markers, {
            imagePath:
              "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
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
      this.wrapper = document.getElementById("wrapper");
      //this.wrapper.style.backgroundImage = `url(${this.url}?center=${this.center.lat},${this.center.lng}&zoom=${this.zoom}&scale=2&size=${this.wrapper.clientWidth}x${this.wrapper.clientHeight}&key=${GOOGLE_MAPS_API_KEY})`;
      //this.wrapper.style.backgroundImage = url("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Grave_eend_maasmuur.jpg/1200px-Grave_eend_maasmuur.jpg");
      console.log(`url(${this.url}?center=${this.center.lat},${this.center.lng}&zoom=${this.zoom}&scale=2&size=${this.wrapper.clientWidth}x${this.wrapper.clientHeight}&key=${GOOGLE_MAPS_API_KEY})`)    
    });
  }
});
