from collections import deque
import time

class CrowdSimulation:
    def __init__(self):
        self.queue = deque()  # Standard Queue (FIFO)
        self.movement_log = []
    
    def add_person(self, person_id, current_node, target_node):
        """Queue mein person add karo"""
        person = {
            'id': person_id,
            'current_node': current_node,
            'target_node': target_node,
            'start_time': time.time()
        }
        self.queue.append(person)
        print(f"✅ Person {person_id} added to queue at Node {current_node}")
    
    def simulate_movement(self, path):
        """Logon ko path ke through move karo"""
        print(f"\n Simulating movement through path: {path}")
        
        while self.queue:
            person = self.queue.popleft()  # FIFO - pehle aaya, pehle gaya
            
            # Har node par 1 second ka delay (simulation ke liye)
            for i, node in enumerate(path):
                person['current_node'] = node
                print(f"  👤 Person {person['id']} at Node {node} (Step {i+1}/{len(path)})")
                time.sleep(0.5)  # Real-time simulation ke liye
            
            # Evacuation complete
            evacuation_time = time.time() - person['start_time']
            self.movement_log.append({
                'person_id': person['id'],
                'evacuation_time': evacuation_time
            })
            print(f"  ✅ Person {person['id']} evacuated in {evacuation_time:.2f} seconds\n")
    
    def get_stats(self):
        """Simulation statistics"""
        if not self.movement_log:
            return "No simulations run yet"
        
        total_time = sum(log['evacuation_time'] for log in self.movement_log)
        avg_time = total_time / len(self.movement_log)
        
        return {
            'total_people_evacuated': len(self.movement_log),
            'average_evacuation_time': f"{avg_time:.2f} seconds",
            'total_evacuation_time': f"{total_time:.2f} seconds"
        }

# Test karne ke liye
if __name__ == '__main__':
    sim = CrowdSimulation()
    
    # 3 logon ko add karo
    sim.add_person(1, 1, 4)  # Person 1: Node 1 se Node 4
    sim.add_person(2, 1, 4)  # Person 2: Node 1 se Node 4
    sim.add_person(3, 1, 4)  # Person 3: Node 1 se Node 4
    
    # Path define karo (Room 101 -> Corridor A -> Main Exit)
    path = [1, 3, 4]
    
    # Simulation chalao
    sim.simulate_movement(path)
    
    # Statistics dikhao
    print("\n📊 Simulation Statistics:")
    stats = sim.get_stats()
    print(stats)