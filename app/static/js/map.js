var app = new Vue({
  el: "#app",
  delimiters: ['[[', ']]'],
  data: {
      search_term: "",
      query_limit: 100,
      hasData: false,
      isLoading: false,
      tweets: [],
      wrapper: null,
      center: { lat: 51.8763, lng: 0.9449 },
      zoom: 15,
      url: "https://maps.googleapis.com/maps/api/staticmap",
      locations: []
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
        console.log(data.positive.details)
        if (data.positive.number > 0) {
          this.hasData = true
          this.tweets = this.tweets.concat(data.positive.details)
        } 
        if (data.negative.number > 0) {
          this.hasData = true
          this.tweets = this.tweets.concat(data.negative.details)
        } 
        if (data.netural.number > 0) {
          this.hasData = true
          this.tweets = this.tweets.concat(data.netural.details)
        } 
        if (this.hasData == false) {
          console.log("No Data to Plot")
        } else {
          console.log(this.tweets)
          this.tweets.forEach(element => {
            try {
              this.locations.push({ lat: element.coordinates[0], lng: element.coordinates[1]})
            } catch (error) {
              console.error(error)
              console.error(element.coordinates)
            }
          });
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
        }
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
