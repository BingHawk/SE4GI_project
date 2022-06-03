<template>
  <div>
    {{ message }} {{particle}} {{value}} 
  </div>
</template>

<script>
export default {
  name: "Popup",
  props: { message: {}, particle: {}, value: {} },
};
</script>
