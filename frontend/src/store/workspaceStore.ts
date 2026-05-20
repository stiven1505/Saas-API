import { create } from 'zustand';

interface Workspace {
  id: string;
  name: string;
  description: string;
  role: 'ADMIN' | 'EDITOR' | 'READER';
}

interface WorkspaceState {
  currentWorkspace: Workspace | null;
  workspaces: Workspace[];
  setCurrentWorkspace: (workspace: Workspace) => void;
  setWorkspaces: (workspaces: Workspace[]) => void;
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  currentWorkspace: null,
  workspaces: [],
  setCurrentWorkspace: (workspace) => set({ currentWorkspace: workspace }),
  setWorkspaces: (workspaces) => set({ workspaces }),
}));
