"use client";

import { create } from "zustand";

type UiState = {
  selectedTab: "featured" | "new" | "budget";
  setSelectedTab: (tab: UiState["selectedTab"]) => void;
};

export const useUiStore = create<UiState>((set) => ({
  selectedTab: "featured",
  setSelectedTab: (tab) => set({ selectedTab: tab })
}));
