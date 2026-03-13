const taskInput = document.getElementById('taskInput');
const addBtn = document.getElementById('addBtn');
const taskList = document.getElementById('taskList');
const counter = document.getElementById('counter');
const clearDoneBtn = document.getElementById('clearDone');
const filterBtns = document.querySelectorAll('.filter');

let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
let currentFilter = 'all';

function save() {
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

function updateCounter() {
  const pending = tasks.filter(t => !t.done).length;
  counter.textContent = `${pending} tarefa${pending !== 1 ? 's' : ''} pendente${pending !== 1 ? 's' : ''}`;
}

function render() {
  const filtered = tasks.filter(t => {
    if (currentFilter === 'pending') return !t.done;
    if (currentFilter === 'done') return t.done;
    return true;
  });

  taskList.innerHTML = '';

  if (filtered.length === 0) {
    taskList.innerHTML = '<p class="empty">Nenhuma tarefa aqui.</p>';
    updateCounter();
    return;
  }

  filtered.forEach(task => {
    const li = document.createElement('li');
    li.className = `task-item${task.done ? ' done' : ''}`;

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = task.done;
    checkbox.id = `task-${task.id}`;
    checkbox.addEventListener('change', () => toggleTask(task.id));

    const label = document.createElement('label');
    label.htmlFor = `task-${task.id}`;
    label.textContent = task.text;

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn';
    deleteBtn.textContent = '✕';
    deleteBtn.title = 'Remover';
    deleteBtn.addEventListener('click', () => removeTask(task.id));

    li.appendChild(checkbox);
    li.appendChild(label);
    li.appendChild(deleteBtn);
    taskList.appendChild(li);
  });

  updateCounter();
}

function addTask() {
  const text = taskInput.value.trim();
  if (!text) return;

  tasks.unshift({ id: Date.now(), text, done: false });
  taskInput.value = '';
  save();
  render();
}

function toggleTask(id) {
  tasks = tasks.map(t => t.id === id ? { ...t, done: !t.done } : t);
  save();
  render();
}

function removeTask(id) {
  tasks = tasks.filter(t => t.id !== id);
  save();
  render();
}

addBtn.addEventListener('click', addTask);
taskInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') addTask();
});

clearDoneBtn.addEventListener('click', () => {
  tasks = tasks.filter(t => !t.done);
  save();
  render();
});

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    render();
  });
});

render();
