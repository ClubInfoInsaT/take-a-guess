export type Player = {
  id: string;
  name: string;
  answer: string;
  hearts: number;
  deathAt: number;
};

export enum AlertLevel {
  INFO = "info",
  DANGER = "danger",
  SUCCESS = "success",
  WARN = "warn",
}
