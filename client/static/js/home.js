new Vue({
  el: "#app",
  data: {
    loading: false,
    username: data.username,
    password: data.password,
    database: data.database,
    collection: ""
  },
  methods: {
    _post: function(url, body) {
      this.loading = true;
      return fetch(url, {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      });
    },
    submit: async function() {
      this.username = this.username.trim();
      this.password = this.password.trim();
      this.database = this.database.trim();
      this.collection = this.collection.trim();

      if (!!this.username && !!this.database && !!this.collection) {
        const response = await this._post("/sign", {
          username: this.username,
          password: this.password || null,
          database: this.database,
          collection: this.collection
        });

        if (response.status === 200) {
          const data = await response.json();
          if (data.error) {
            this.loading = false;
            return alert(data.error);
          }

          window.location.href = "/collections/" + this.collection;
        }
      } else {
        alert("username, database and collection fields are required");
      }
    }
  }
});
