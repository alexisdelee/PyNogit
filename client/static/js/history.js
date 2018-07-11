new Vue({
  el: "#app",
  data: {
    loading: false,
    commits: data.commits
  },
  methods: {
    _put: function(url, body, method = "PUT") {
      this.loading = true;
      return fetch(url, {
        method: method,
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });
    },
    parse: function(value) {
      try {
        return JSON.parse("{\"a\": " + value + "}");
      } catch(e) {
        return null;
      }
    }
  }
});
