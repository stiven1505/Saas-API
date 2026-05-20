import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField
} from '@mui/material';

import api from '../api/axios';
import { useWorkspaceStore } from '../store/workspaceStore';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const { currentWorkspace } = useWorkspaceStore();
  const navigate = useNavigate();

  // Dialog state
  const [open, setOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');

  useEffect(() => {
    if (!currentWorkspace) {
      navigate('/workspaces');
      return;
    }

    const fetchProjects = async () => {
      try {
        setLoading(true);

        const response = await api.get('/projects');
        setProjects(response.data);

      } catch (err) {
        console.error('Failed to fetch projects', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, [currentWorkspace, navigate]);

  const handleCreateProject = async () => {
    if (!newProjectName) return;

    try {
      await api.post('/projects', {
        name: newProjectName,
        description: newProjectDesc,
        status: 'ACTIVE'
      });

      setOpen(false);
      setNewProjectName('');
      setNewProjectDesc('');

      // refresh list
      const response = await api.get('/projects');
      setProjects(response.data);

    } catch (err) {
      console.error('Failed to create project', err);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>

      {/* HEADER */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4">Projects</Typography>

        {currentWorkspace?.role === 'ADMIN' || currentWorkspace?.role === 'EDITOR' ? (
          <Button
            variant="contained"
            color="primary"
            onClick={() => setOpen(true)}
          >
            New Project
          </Button>
        ) : null}
      </Box>

      {/* PROJECT LIST */}
      <Grid container spacing={3}>
        {projects.map((project: any) => (
          <Grid item xs={12} md={6} key={project.id}>
            <Card>
              <CardContent>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6">{project.name}</Typography>

                  <Chip
                    label={project.status}
                    color={project.status === 'ACTIVE' ? 'success' : 'default'}
                    size="small"
                  />
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {project.description || 'No description'}
                </Typography>


              </CardContent>
            </Card>
          </Grid>
        ))}

        {projects.length === 0 && (
          <Grid item xs={12}>
            <Typography variant="body1" color="text.secondary">
              No projects found in this workspace.
            </Typography>
          </Grid>
        )}
      </Grid>

      {/* CREATE PROJECT DIALOG */}
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New Project</DialogTitle>

        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Project Name"
            fullWidth
            value={newProjectName}
            onChange={(e) => setNewProjectName(e.target.value)}
          />

          <TextField
            margin="dense"
            label="Description (Optional)"
            fullWidth
            multiline
            rows={3}
            value={newProjectDesc}
            onChange={(e) => setNewProjectDesc(e.target.value)}
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setOpen(false)}>
            Cancel
          </Button>

          <Button
            variant="contained"
            onClick={handleCreateProject}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>

    </Box>
  );
}