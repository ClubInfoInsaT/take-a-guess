<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script lang="ts">
import Vue from "vue";
import NoSleep from "nosleep.js";

export default Vue.extend({
  mounted: function () {
    const noSleep = new NoSleep();
    // Enable wake lock.
    // (must be wrapped in a user input event handler e.g. a mouse or touch handler)
    document.addEventListener(
      "click",
      function enableNoSleep() {
        document.removeEventListener("click", enableNoSleep, false);
        noSleep.enable();
        console.log("Mounted and no sleep !!");
      },
      false
    );

    // Emit a disconnect event when the client leave the page
    window.addEventListener("beforeunload", () => {
      this.$socket.disconnect();
    });
  },
});
</script>
