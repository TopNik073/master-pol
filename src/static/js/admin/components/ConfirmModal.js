export class ConfirmModal {
    constructor() {
      this.modalId = 'confirmModal';
      this.initModal();
    }
  
    initModal() {
      const modalHtml = `
        <div class="modal fade" id="${this.modalId}" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header border-0 pb-0">
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body text-center px-4 pb-4 pt-0">
                <div class="mb-3" style="font-size: 3rem; color: #ff6b6b;">
                  <i class="fas fa-exclamation-circle"></i>
                </div>
                <h5 class="modal-title mb-3" id="${this.modalId}Label">Вы уверены?</h5>
                <p class="mb-4">Это действие нельзя будет отменить. Удаление будет выполнено безвозвратно.</p>
              </div>
              <div class="modal-footer border-0 justify-content-center">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="button" class="btn btn-danger" id="${this.modalId}ConfirmBtn">Удалить</button>
              </div>
            </div>
          </div>
        </div>
      `;
  
      document.body.insertAdjacentHTML('beforeend', modalHtml);
      this.modalElement = document.getElementById(this.modalId);
      this.confirmButton = document.getElementById(`${this.modalId}ConfirmBtn`);
    }
  
    show() {
      return new Promise((resolve) => {
        const modalInstance = new bootstrap.Modal(this.modalElement);
        
        const handleConfirm = () => {
          this.confirmButton.removeEventListener('click', handleConfirm);
          modalInstance.hide();
          resolve(true);
        };
  
        const handleHide = () => {
          this.modalElement.removeEventListener('hidden.bs.modal', handleHide);
          resolve(false);
        };
  
        this.confirmButton.addEventListener('click', handleConfirm);
        this.modalElement.addEventListener('hidden.bs.modal', handleHide);
        
        modalInstance.show();
      });
    }
  }