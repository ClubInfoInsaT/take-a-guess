<template>
  <div
    class="flex p-4 mb-4 text-sm rounded-lg text-blue-800 opacity-100"
    :class="background() + ' ' + text()"
    role="alert"
  >
    <font-awesome-icon
      fill="currentColor"
      :icon="iconName()"
      class="inline flex-shrink-0 mr-1 w-5 h-5"
    />
    <div>
      <span class="font-medium">{{ title }}</span> {{ description }}
    </div>
  </div>
</template>

<script lang="ts">
import { AlertLevel } from "@/constants/types";
import { Component, Vue, Prop } from "vue-property-decorator";

@Component
export default class Alert extends Vue {
  @Prop({ required: true }) readonly title!: string;
  @Prop({ required: true }) readonly description!: string;
  @Prop({ required: true, default: AlertLevel.INFO })
  readonly level!: AlertLevel;

  alert!: Element | null;

  mounted() {
    this.alert = document.querySelector("div[role=alert]");
  }

  iconName(): string {
    switch (this.level) {
      default:
      case AlertLevel.INFO: {
        return "fa-solid fa-info";
      }
      case AlertLevel.WARN: {
        return "fa-solid fa-triangle-exclamation";
      }
      case AlertLevel.SUCCESS: {
        return "fa-solud fa-check";
      }
      case AlertLevel.DANGER: {
        return "fa-solid fa-xmark";
      }
    }
  }

  text(): string {
    switch (this.level) {
      default:
      case AlertLevel.INFO: {
        return "text-blue-700";
      }
      case AlertLevel.WARN: {
        return "text-yellow-700";
      }
      case AlertLevel.SUCCESS: {
        return "text-green-700";
      }
      case AlertLevel.DANGER: {
        return "text-red-700";
      }
    }
  }

  background(): string {
    switch (this.level) {
      default:
      case AlertLevel.INFO: {
        return "bg-blue-200";
      }
      case AlertLevel.WARN: {
        return "bg-yellow-200";
      }
      case AlertLevel.SUCCESS: {
        return "bg-green-200";
      }
      case AlertLevel.DANGER: {
        return "bg-red-200";
      }
    }
  }
}
</script>

<style></style>
