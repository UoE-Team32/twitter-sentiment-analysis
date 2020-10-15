var app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        search_term: "",
        query_limit: 100,
        data: [],
        overallPieChart: null,
        isLoading: false,
        tweets: null
    },
    methods: {
      async query() {
        // Set loading to opposite of itself
        this.isLoading = !this.isLoading;

        // Fetch the tweets based on the query
        await query_tweets(this.search_term, this.query_limit).then((data) => {
          this.tweets = data;
        }).catch((err) => {
          console.error(err);
        });

        // It is real hacky, but its a challenge so things shouldnt be done properly in the first place! :)
        this.data[0] = this.tweets.positive.number;
        this.data[1] = this.tweets.netural.number;
        this.data[2] = this.tweets.negative.number;

        // Update the Pie chart
        var chart = this.overallPieChart; // I am lazy...
        chart.data.datasets.forEach((dataset) => {
          dataset.data.push(this.data);
        });
        chart.update();

        // Some more hacky code! Update the table values
        document.getElementById("pos").innerHTML = this.data[0];
        document.getElementById("neu").innerHTML = this.data[1];
        document.getElementById("neg").innerHTML = this.data[2];

        // Reset loading
        this.isLoading = !this.isLoading;
      },
    },
    mounted() {
      // Pie chart data
      var data = ({
        datasets: [
          {
            data: this.data,  
            backgroundColor: ['#48c774', '#e6e6e6', '#f14668']
          },
        ],
        
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: ["Positive", "Neutral", "Negative"],
      });

      this.overallPieChart = new Chart(document.getElementById("positiveChart").getContext("2d"), {
        type: 'pie',
        data: data
      })
    }
  });
