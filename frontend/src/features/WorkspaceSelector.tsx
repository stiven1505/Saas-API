import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Card, CardContent, CardActions, Button, Grid, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import api from '../api/axios';
import { useWorkspaceStore } from '../store/workspaceStore';

export default function WorkspaceSelector() {
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [newWorkspaceName, setNewWorkspaceName] = useState('');
  const [newWorkspaceDesc, setNewWorkspaceDesc] = useState('');
  const { workspaces, setWorkspaces, setCurrentWorkspace } = useWorkspaceStore();
  const navigate = useNavigate();

  const fetchWorkspaces = async () => {
    try {
      const response = await api.get('/workspaces');
      setWorkspaces(response.data);
    } catch (err) {
      console.error('Failed to fetch workspaces', err);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    const fetchWorkspaces = async () => {
      try {
        setLoading(true);


        const response = await api.get('/workspaces');


        setWorkspaces(response.data);
      } catch (err) {
        console.error("ERROR FETCHING WORKSPACES", err);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkspaces();
  }, [setWorkspaces]);

  const handleSelect = (workspace: any) => {
    setCurrentWorkspace(workspace);
    navigate('/');
  };

  const handleCreate = async () => {
    if (!newWorkspaceName) return;
    try {
      await api.post('/workspaces', { name: newWorkspaceName, description: newWorkspaceDesc });
      setOpen(false);
      setNewWorkspaceName('');
      setNewWorkspaceDesc('');
      await fetchWorkspaces(); // refresh list
    } catch (err) {
      console.error('Failed to create workspace', err);
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">
          Select a Workspace
        </Typography>
        <Button variant="contained" color="primary" onClick={() => setOpen(true)}>
          Create Workspace
        </Button>
      </Box>
      
      <Grid container spacing={3}>
        {workspaces.map((ws: any) => {
          return (
            <Grid item xs={12} sm={6} md={4} key={ws.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{ws.name}</Typography>

                  <Typography variant="body2" color="text.secondary">
                    {ws.description || 'No description'}
                  </Typography>
                </CardContent>

                <CardActions>
                  <Button size="small" variant="contained" onClick={() => handleSelect(ws)}>
                    Enter Workspace
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          );
        })}
        {
        workspaces.length === 0 && (
          <Grid item xs={12}>
            <Typography>You are not a member of any workspaces. Create one to get started!</Typography>
          </Grid>
        )}
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Workspace</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Workspace Name"
            type="text"
            fullWidth
            value={newWorkspaceName}
            onChange={(e) => setNewWorkspaceName(e.target.value)}
            required
          />
          <TextField
            margin="dense"
            label="Description (Optional)"
            type="text"
            fullWidth
            multiline
            rows={3}
            value={newWorkspaceDesc}
            onChange={(e) => setNewWorkspaceDesc(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleCreate} variant="contained" color="primary">Create</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
