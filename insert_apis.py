# insert_apis.py - app.py ga API'larni qo'shish scripti
import re

# Yangi API kodlari
new_apis = '''
# NOTIFICATION VA COIN BOSHQARUV API'LARI
@app.route('/admin/add_coins_to_user/<int:user_id>', methods=['POST'])
@login_required
def add_coins_to_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin huquqi yo\\'q'})
    
    try:
        data = request.get_json()
        coins_amount = data.get('coins', 0)
        reason = data.get('reason', 'Admin tomonidan qo\\'shildi')
        
        if coins_amount <= 0 or coins_amount > 10000:
            return jsonify({'success': False, 'error': 'Coin miqdori 1 dan 10000 gacha bo\\'lishi kerak'})
        
        user = User.query.get_or_404(user_id)
        user.coins += coins_amount
        
        # Notification yaratish
        notification = Notification(
            user_id=user_id,
            title='💰 Coin olindi!',
            message=f'Sizga {coins_amount} coin qo\\'shildi! Sabab: {reason}',
            notification_type='coin',
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'{user.username}ga {coins_amount} coin qo\\'shildi',
            'new_balance': user.coins
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get_notifications')
@login_required
def get_notifications():
    try:
        notifications = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).order_by(Notification.created_at.desc()).limit(10).all()
        
        return jsonify({
            'success': True,
            'notifications': [{
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.notification_type,
                'created_at': n.created_at.isoformat()
            } for n in notifications]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    try:
        notification = Notification.query.get_or_404(notification_id)
        if notification.user_id == current_user.id:
            notification.is_read = True
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Ruxsat berilmagan'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

'''

# app.py ni o'qish
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# "def init_database()" oldida qo'shish
pattern = r'(def init_database\(\):)'
replacement = new_apis + r'\n\1'

if 'def add_coins_to_user' in content:
    print("✅ API'lar allaqachon qo'shilgan!")
else:
    content = re.sub(pattern, replacement, content)
    
    # Yangilangan faylni saqlash
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ API'lar muvaffaqiyatli qo'shildi!")
