<template>
  <div class="flex flex-row text-white text-2xl">
    <div class="w-1/5 text-center">{{ position + 1 }}</div>
    <div class="w-2/5">{{ player.name }}</div>
    <div class="w-1/5">
      <div class="flex flex-row items-center gap-x-2">
        <font-awesome-icon
          icon="fa-regular fa-heart"
          v-for="i in maxHearts - player.hearts"
          :key="player.name + 'broken-' + i"
        />

        <font-awesome-icon
          icon="fa-solid fa-heart"
          v-for="j in player.hearts"
          :key="player.name + 'alive-' + j"
        />
      </div>
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
