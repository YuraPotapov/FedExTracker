<template>
  <div>
    <h1>FedEx Tracking</h1>
    <input v-model="trackingNumber" type="text" placeholder="Enter tracking number" />
    <button @click="submitTracking">Submit</button>
    <pre>{{ trackingResult }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      trackingNumber: "",
      trackingResult: "",
    };
  },
  methods: {
    async submitTracking() {
      try {
        const response = await fetch(`http://localhost:8001/track/${this.trackingNumber}`);
        const data = await response.json();
        this.trackingResult = JSON.stringify(data, null, 2);
      } catch (error) {
        alert(error);
      }
    },
  },
};
</script>
