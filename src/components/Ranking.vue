<template>
  <div class="flex flex-row text-white md:text-2xl text-lg">
    <div class="w-1/5 text-center">{{ position + 1 }}</div>
    <div class="w-2/5">{{ player.name }}</div>
    <div class="w-1/5 flex flex-row items-center gap-x-1 justify-center">
      {{ player.hearts }}<font-awesome-icon icon="fa-solid fa-heart" />
    </div>
    <div class="w-1/5 text-center">{{ player.deathAt }}</div>
  </div>
</template>
<script lang="ts">
import { Player } from "@/constants/types";
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class Ranking extends Vue {
  @Prop({ required: true })
  readonly position!: number;

  @Prop({ required: true })
  readonly player!: Player;

  @Prop({ required: true })
  readonly maxHearts!: number;
}
</script>
