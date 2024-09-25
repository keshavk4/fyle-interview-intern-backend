@app.route('/principal/assignments', methods=['GET'])
def get_assignments_principal():
    principal_id = request.headers.get('X-Principal')
    if not principal_id:
        return jsonify({'message': 'Principal authorization required'}), 401

    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    data = [assignment.to_dict() for assignment in assignments]
    return jsonify({'data': data}), 200

@app.route('/principal/teachers', methods=['GET'])
def get_teachers_principal():
    principal_id = request.headers.get('X-Principal')
    if not principal_id:
        return jsonify({'message': 'Principal authorization required'}), 401

    teachers = User.query.filter_by(role='TEACHER').all()
    data = [teacher.to_dict() for teacher in teachers]
    return jsonify({'data': data}), 200

@app.route('/principal/assignments/grade', methods=['POST'])
def grade_assignment_principal():
    principal_id = request.headers.get('X-Principal')
    if not principal_id:
        return jsonify({'message': 'Principal authorization required'}), 401
    
    data = request.get_json()
    assignment_id = data.get('id')
    new_grade = data.get('grade')

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({'message': 'Assignment not found'}), 404

    assignment.grade = new_grade
    assignment.state = 'GRADED'
    db.session.commit()

    return jsonify({'data': assignment.to_dict()}), 200
