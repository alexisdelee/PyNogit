new Vue({
  el: "#app",
  data: {
    collection: data.collection,
    loading: false,
    editionMode: {
      enable: false,
      blob: null,
      key: null,
      value: null,
      error: false,
      isInsertion: false
    },
    blobs: data.blobs
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
    _delete: function(url, body) {
      return this._put(url, body, "DELETE");
    },
    insert: async function() {
      this.editionMode = {
        enable: false,
        blob: null,
        key: document.querySelector(".insertMode td:first-child").textContent,
        value: document.querySelector(".insertMode td:nth-child(2)").textContent,
        error: false,
        isInsertion: true
      };

      this.editionMode.error = false;
      if (!this.editionMode.key || !this.editionMode.value) {
        return alert("key and value fields are required");
      }

      const data = this.parse(this.editionMode.value);
      if (data === null) {
        return this.editionMode.error = true;
      }

      this.editionMode.value = this.parse(this.editionMode.value).a;

      const response = await this._put("/blobs", {
        collection: this.collection,
        key: this.editionMode.key,
        value: this.editionMode.value
      });

      if (response.status === 200) {
        const data = await response.json();
        if (data.error) {
          this.loading = false;
          return alert(data.error);
        }

        window.location.reload();
      }
    },
    edit: function(blob, key) {
      this.editionMode = {
        enable: true,
        blob: blob,
        key: key,
        value: blob.value,
        error: false,
        isInsertion: false
      };
    },
    parse: function(value) {
      try {
        return JSON.parse("{\"a\": " + value + "}");
      } catch(e) {
        return null;
      }
    },
    edition: function(e) {
      this.editionMode.value = document.querySelector("#editionMode").textContent;
      this.editionMode.error = false;

      const response = this.parse(this.editionMode.value);
      if (response === null) {
        this.editionMode.error = true;
      } else {
        return this.submit();
      }
    },
    submit: async function() {
      // console.log(this.editionMode.key, this.parse(this.editionMode.value).a);
      this.editionMode.blob.value = this.parse(this.editionMode.value).a;

      const response = await this._put("/blobs", {
        collection: this.collection,
        key: this.editionMode.key,
        value: this.editionMode.blob.value
      });

      if (response.status === 200) {
        const data = await response.json();
        if (data.error) {
          this.loading = false;
          return alert(data.error);
        }

        window.location.reload();
      }
    },
    remove: async function(key) {
      const response = await this._delete("/blobs", {
        collection: this.collection,
        key: key
      });

      if (response.status === 200) {
        const data = await response.json();
        if (data.error) {
          this.loading = false;
          return alert(data.error);
        }

        window.location.reload();
      }
    },
    setExpire: async function (blob, key) {
      do {
        var seconds = prompt("Set seconds before expiration or -1");
        if (!seconds) {
          return;
        } else if (isNaN(seconds)) {
          continue;
        }

        seconds = parseInt(seconds);
      } while(isNaN(seconds) || (isNaN(seconds) === false && seconds < -1));

      const response = await this._put("/blobs/expire", {
        collection: this.collection,
        key: key,
        seconds: seconds
      });

      if (response.status === 200) {
        const data = await response.json();
        if (data.error) {
          this.loading = false;
          return alert(data.error);
        }

        window.location.reload();
      }
    }
  }
});
